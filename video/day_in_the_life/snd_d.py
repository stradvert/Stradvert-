# Score + sound design for a story-led minimal edit. Everything is synthesised (no samples, no licences).
# The music follows the story: tension, a light groove, hard stops for the punchlines. Reads data.json (segment times), writes music.wav and sfx.wav.
import numpy as np,json,wave,os
MUSIC=os.environ.get('MUSIC','1')!='0'      # MUSIC=0: no score and nothing tonal, only the effects track
from scipy.signal import butter,sosfilt,sosfilt_zi,fftconvolve
sr=48000;D=json.load(open('data.json'));SG=D['segs'];TOTAL=D['total']/30.0;VD=D['vd'];N=int(sr*(TOTAL+0.5))
rng=np.random.default_rng(5)
T=lambda k,o=0.0:SG[k][0]+o
E=lambda k,o=0.0:SG[k][1]+o
BPM=106.0;BEAT=60/BPM
# ---------------- helpers ----------------
def note(m):return 440.0*2**((m-69)/12)
def st(x,p=0.0):
    a=(p+1)*np.pi/4;return np.stack([x*np.cos(a),x*np.sin(a)],1)
def bq(x,kind,fc,order=2,fc2=None):
    if kind=='bp':sos=butter(order,[fc/(sr/2),fc2/(sr/2)],btype='band',output='sos')
    else:sos=butter(order,min(0.99,fc/(sr/2)),btype={'lp':'low','hp':'high'}[kind],output='sos')
    return sosfilt(sos,x,axis=0)
def tvlp(x,fcs,order=2,blk=256):
    y=np.empty_like(x);zi=None
    for i in range(0,len(x),blk):
        fc=float(np.clip(fcs[min(i,len(fcs)-1)],30,sr*0.45));sos=butter(order,fc/(sr/2),output='sos')
        if zi is None:zi=sosfilt_zi(sos)*x[0]
        y[i:i+blk],zi=sosfilt(sos,x[i:i+blk],zi=zi)
    return y
def add(buf,x,t,g=1.0):
    i=int(round(t*sr))
    if i<0:x=x[-i:];i=0
    n=min(len(x),len(buf)-i)
    if n>0:buf[i:i+n]+=x[:n]*g
def reverb(x,decay=1.4,pre=0.012,lp=4800,hp=220,seed=1):
    r=np.random.default_rng(seed);n=int(decay*sr);t=np.arange(n)/sr
    ir=np.stack([r.standard_normal(n),r.standard_normal(n)],1)*np.exp(-t*6.9/decay)[:,None]
    ir=bq(bq(ir,'lp',lp),'hp',hp);ir[:int(0.004*sr)]*=np.linspace(0,1,int(0.004*sr))[:,None];ir/=np.sqrt((ir**2).sum(0)).mean()
    xs=x if x.ndim==2 else st(x);out=np.stack([fftconvolve(xs[:,0],ir[:,0]),fftconvolve(xs[:,1],ir[:,1])],1)
    return np.concatenate([np.zeros((int(pre*sr),2)),out],0)
# ---------------- instruments ----------------
def ep(m,dur=0.9,vel=0.7):
    """soft electric piano: FM bell on the attack, mellow body"""
    f=note(m);n=int((dur+0.5)*sr);t=np.arange(n)/sr
    x=np.sin(2*np.pi*f*t+np.sin(2*np.pi*f*t)*(2.0*vel)*np.exp(-t*7))+0.22*np.sin(2*np.pi*2*f*t)*np.exp(-t*4)
    env=np.clip(t/0.004,0,1)*np.exp(-t*2.4)*np.where(t>dur,np.exp(-(t-dur)*14),1.0)
    return bq(x*env*(1+0.06*np.sin(2*np.pi*4.6*t)),'lp',3000)*vel
def bassn(m,dur=0.5,vel=0.8):
    f=note(m);n=int((dur+0.15)*sr);t=np.arange(n)/sr
    x=np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*5)+0.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*9)
    env=np.clip(t/0.008,0,1)*np.exp(-t*1.6)*np.clip((dur+0.15-t)/0.08,0,1)
    return np.tanh(x*env*1.4)*vel
def kick(g=1.0):
    n=int(0.34*sr);t=np.arange(n)/sr;f=44+72*np.exp(-t*30);x=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*10)
    return bq(np.tanh((x+bq(rng.standard_normal(n),'lp',1800)*np.exp(-t*260)*0.2)*1.3),'lp',2400)*g
def rim(g=1.0):
    n=int(0.07*sr);t=np.arange(n)/sr;x=np.sin(2*np.pi*1750*t)*np.exp(-t*95)+0.5*bq(rng.standard_normal(n),'bp',2200,2,6000)*np.exp(-t*130)
    return x*g
def shaker(g=1.0,dec=58):
    n=int(0.08*sr);t=np.arange(n)/sr;return bq(rng.standard_normal(n),'hp',6500)*np.clip(t/0.004,0,1)*np.exp(-t*dec)*g
def tamb(g=1.0):
    n=int(0.14*sr);t=np.arange(n)/sr;x=bq(rng.standard_normal(n),'hp',8000)*(np.exp(-t*40)+0.6*np.exp(-np.abs(t-0.022)*160))
    return x*g*0.6
def pluck(m,dur=0.6,bright=0.5):
    f=note(m);n=int(dur*sr);P=int(sr/f);buf=bq(rng.standard_normal(P),'lp',1500+3500*bright);out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%P];buf[i%P]=0.5*(buf[i%P]+buf[(i+1)%P])*0.993
    return out*np.exp(-np.arange(n)/sr*4)
# ---------------- harmony ----------------
CH=[([53,57,60,64],41),([52,55,59,62],40),([50,53,57,60],38),([55,60,62,65],43)]     # Fmaj7, Em7, Dm7, G7sus (keys, bass root)
LEAD=[[(0.0,76),(0.75,79),(1.5,81),(2.5,79)],[(0.0,74),(1.0,76),(2.0,79),(3.25,76)],[(0.0,72),(0.75,76),(1.5,77),(2.5,76)],[(0.5,74),(1.5,77),(2.5,79),(3.5,74)]]
def groove(t0,t1,kind=1,bar0=0,drums=True,keys=True,bass=True,lead=False,level=1.0):
    """one section of the groove into its own buffer; the bar grid starts at t0. kind 1 = easy, 2 = bike (offbeat stabs, busier bass)"""
    n=int((t1-t0+1.2)*sr);k=np.zeros((n,2));b=np.zeros(n);d=np.zeros((n,2));l=np.zeros((n,2))
    nb=int(np.ceil((t1-t0)/BEAT))
    for q in range(nb*2):                       # 8th-note steps
        tb=q*BEAT/2
        if tb>=t1-t0-0.01:break
        bar=bar0+q//8;s8=q%8;notes,root=CH[bar%4];beat=s8/2
        if keys:
            if kind==1:
                if s8==0:
                    for i,m in enumerate(notes):add(k,st(ep(m,BEAT*1.7,0.55),-0.25+0.1*i),tb,0.5)
                if s8 in(3,5):
                    for i,m in enumerate(notes[1:]):add(k,st(ep(m+12 if s8==5 and i==2 else m,BEAT*0.3,0.42),0.2),tb,0.42)
            else:
                if s8==0:
                    for m in notes[:2]:add(k,st(ep(m,BEAT*0.9,0.4),-0.2),tb,0.42)
                if s8%2==1:
                    for i,m in enumerate(notes[1:]):add(k,st(ep(m,BEAT*0.22,0.5),0.25),tb,0.5)
        if bass:
            if kind==1:pat={0:(root,0.9),3:(root,0.35),4:(root+7,0.7),6:(root,0.4),7:(root+4,0.3)}
            else:pat={0:(root,0.4),1:(root,0.3),2:(root+4,0.4),3:(root+7,0.3),4:(root+12,0.4),5:(root+7,0.3),6:(root+4,0.4),7:(root+7,0.3)}
            if s8 in pat:add(b,bassn(pat[s8][0],BEAT*pat[s8][1],0.8),tb,0.5)
        if drums:
            if s8 in(0,4):add(d,st(kick(0.8)),tb,0.5)
            if kind==2 and s8==5:add(d,st(kick(0.5)),tb,0.4)
            if s8 in(2,6):add(d,st(rim(0.8),-0.15),tb,0.34)
            if kind==2 and s8 in(2,6):add(d,st(tamb(0.7),0.3),tb,0.3)
            add(d,st(shaker(0.55 if s8%2 else 0.3),0.35),tb,0.26)
        if lead:
            for (bt,m) in LEAD[bar%4]:
                if abs(bt-beat)<1e-6 or (bt*2)%1 and abs(bt-beat-0.25)<1e-6:add(l,st(pluck(m,0.7,0.45),-0.3 if (bar+s8)%2 else 0.3),tb+(bt-beat)*BEAT,0.2)
    k=k+0.3*reverb(k,1.3,seed=3)[:n];dl=int(0.75*BEAT*sr);echo=np.zeros_like(l);echo[dl:,0]=l[:-dl,1]*0.4;echo[dl:,1]=l[:-dl,0]*0.4;l=bq(l+echo,'lp',3600);l=l+0.3*reverb(l,1.5,seed=7)[:n]
    d=d+0.12*reverb(bq(d,'hp',500),0.7,seed=9)[:n]
    return (k*0.9+st(b)*0.9+d*0.9+l)*level,n
def place(buf,sec,t0,t1,fin=0.005,fout=0.05,lp=None):
    """put a section into the mix; fout is the fade at its end (short = hard stop). lp = (start Hz, end Hz) closes a filter across the section"""
    x,n=sec;m=int((t1-t0)*sr);x=x[:max(m,1)+int(0.9*sr)].copy();g=np.ones(len(x))
    a=int(fin*sr);g[:a]=np.linspace(0,1,a);o=int(fout*sr);g[m-o:m]=np.linspace(1,0,o) if m-o>=0 else g[m-o:m];g[m:]=0
    if lp:
        fc=np.geomspace(lp[0],lp[1],m);fc=np.concatenate([fc,np.full(len(x)-m,lp[1])]);x=np.stack([tvlp(x[:,0],fc),tvlp(x[:,1],fc)],1)
    add(buf,x*g[:,None],t0)
music=np.zeros((N,2));sfx=np.zeros((N,2))
if MUSIC:
    # ---------------- A: hook. Low tension bed, then a quick run ----------------
    def drone(t0,t1,notes=(38,45,50,53),lo=380,hi=900,g=1.0):
        n=int((t1-t0)*sr);t=np.arange(n)/sr;y=np.zeros((n,2))
        for m in notes:
            for ch in(0,1):
                for dt in rng.uniform(-12,12,3):y[:,ch]+=2*((note(m)*2**(dt/1200)*t+rng.uniform())%1)-1
        fc=np.linspace(lo,hi,n);y=np.stack([tvlp(y[:,0],fc,4),tvlp(y[:,1],fc,4)],1)
        e=np.clip(t/0.25,0,1)*np.clip((t1-t0-t)/0.12,0,1)*(1+0.12*np.sin(2*np.pi*5.5*t));add(music,y*e[:,None],t0,0.035*g)
    drone(0.0,T('r1',-0.13),g=1.6)
    for i,tt in enumerate(np.arange(T('h2'),T('r1',-0.16),0.094)):add(music,st(shaker(0.5+0.03*i,70),0.3 if i%2 else -0.3),tt,0.42)
    for tt in np.arange(T('h2'),T('r1',-0.2),0.376):add(music,st(kick(0.8)),tt,0.6)
    # ---------------- B: the plan. Easy groove ----------------
    place(music,groove(T('r1'),T('b1'),kind=1,bar0=0,level=1.0),T('r1'),T('b1'),fout=0.02)
    # ---------------- C: heard shouting (filter closes), buffalo (held breath), run ----------------
    place(music,groove(T('b1'),T('b2'),kind=1,bar0=3,drums=False,level=0.9),T('b1'),T('b2'),fout=0.25,lp=(2600,260))
    drone(T('b2'),T('b3'),notes=(38,39,45),lo=300,hi=520,g=0.9)
    for i,tt in enumerate(np.arange(T('b3'),T('b6',-0.05),0.094)):add(music,st(shaker(0.5+0.02*i,70),0.3 if i%2 else -0.3),tt,0.42)
    for tt in np.arange(T('b3'),T('b6',-0.1),0.376):add(music,st(kick(0.8)),tt,0.6)
    # D: "I'm gonna have to walk back now and get a bike" plays dry
    # ---------------- E: plan B, the bike. Busier groove, thins out for the reveal, stops for the punchline ----------------
    place(music,groove(T('k1'),T('k3'),kind=2,bar0=0,level=1.0),T('k1'),T('k3'),fout=0.03)
    place(music,groove(T('k3'),T('k5'),kind=2,bar0=1,drums=False,level=0.62),T('k3'),T('k5'),fout=0.12,lp=(1700,700))
    # ---------------- F: the ride, then the work day (lead joins) until "Never again" ----------------
    place(music,groove(T('d1'),T('w2a'),kind=2,bar0=2,level=1.0),T('d1'),T('w2a'),fout=0.03)
    place(music,groove(T('w2a'),T('z1'),kind=1,bar0=0,lead=True,level=0.95),T('w2a'),T('z1'),fout=0.07)
    # ---------------- G: end card. One warm chord ----------------
    for i,m in enumerate((48,55,62,64,67)):add(music,st(ep(m,2.0,0.6),-0.3+0.15*i),VD+0.02+i*0.035,0.5)
    add(music,st(bassn(36,1.6,0.8)),VD+0.02,0.5)
    tail=reverb(music[int(VD*sr):int((VD+0.6)*sr)],2.2,seed=11);add(music,tail,VD,0.25)
    music=bq(music,'lp',9500)

# ---------------- sound effects ----------------
def boom(t,g=1.0,f0=58,tail=1.1,p=0.0):
    n=int(tail*sr);x=np.arange(n)/sr;f=f0*np.exp(-x*2.6)+30;y=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-x*3.6)
    th=bq(rng.standard_normal(n),'bp',70,2,380)*np.exp(-x*18)*1.0;s=st(np.tanh((y+th)*1.3),p);add(sfx,s,t,g*0.6);add(sfx,reverb(bq(s,'hp',160),1.6,lp=2400,seed=int(t*100)%97+2),t,g*0.12)
def whoosh(t_end,dur=0.36,g=1.0,lo=350,hi=4800,p0=-0.6,p1=0.6):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=lo+(hi-lo)*x**2.2;y=tvlp(y,fc,2)-tvlp(y,fc*0.35,2)
    e=x**2.2*np.clip((1-x)/0.06,0,1);p=p0+(p1-p0)*x;a=(p+1)*np.pi/4;add(sfx,np.stack([y*e*np.cos(a),y*e*np.sin(a)],1),t_end-dur,g*0.4)
def swish(t,dur=0.28,g=1.0,p0=0.5,p1=-0.5):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=900+3400*np.sin(np.pi*x)**2;y=tvlp(y,fc,2)-tvlp(y,fc*0.4,2)
    e=np.sin(np.pi*x)**2;p=p0+(p1-p0)*x;a=(p+1)*np.pi/4;add(sfx,np.stack([y*e*np.cos(a),y*e*np.sin(a)],1),t-dur*0.45,g*0.34)
def tick(t,g=1.0,f=2100,p=0.0):
    n=int(0.05*sr);x=np.arange(n)/sr;y=(np.sin(2*np.pi*f*x)+0.4*bq(rng.standard_normal(n),'hp',4000))*np.exp(-x*150);add(sfx,st(y,p),t,g*0.1)
def pop(t,g=1.0,f=520,p=0.0):
    n=int(0.13*sr);x=np.arange(n)/sr;y=np.sin(2*np.pi*np.cumsum(f*(1+0.9*np.exp(-x*60)))/sr)*np.exp(-x*34);add(sfx,st(y,p),t,g*0.2)
def key(t,g=1.0):
    n=int(0.035*sr);x=np.arange(n)/sr;y=bq(rng.standard_normal(n),'bp',1500,2,5000)*np.exp(-x*170)+0.4*np.sin(2*np.pi*310*x)*np.exp(-x*120);add(sfx,st(y,rng.uniform(-0.2,0.2)),t,g*0.16)
def rewind(t_end,dur=0.3,g=1.0):
    n=int(dur*sr);x=np.arange(n)/n;f=300*2**(x*2.6);y=np.sin(2*np.pi*np.cumsum(f)/sr)*0.5+bq(rng.standard_normal(n),'bp',900,2,5200)*0.5
    y*=(0.55+0.45*np.sign(np.sin(2*np.pi*26*x)))*np.sin(np.pi*x)**0.7;add(sfx,st(y),t_end-dur,g*0.22)
def bell(t,notes=(79,84),g=1.0):
    for i,m in enumerate(notes):
        n=int(1.4*sr);x=np.arange(n)/sr;f=note(m);y=(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*2.76*f*x)*np.exp(-x*6))*np.exp(-x*4.4)*np.clip(x/0.004,0,1)
        s=st(y,-0.3+0.6*i);add(sfx,s,t+i*0.085,g*0.07);add(sfx,reverb(s,1.6,lp=6500,seed=51+i),t+i*0.085,g*0.025)
P=D['pills'];C=D['cards'];L=D['lists'][0];Q=1.0 if MUSIC else 0.7
if not MUSIC:
    def bell(*a,**k):pass                     # bells are tonal: out with the music
boom(0.0,0.75*Q);tick(P[0]['wipe'],0.9,p=-0.2);pop(P[1]['s'],0.5,640)
whoosh(T('h2')+0.02,0.3,0.9,p0=0.6,p1=-0.6);rewind(T('r1'),0.3,1.0)
tick(P[2]['s']+0.05,0.6);whoosh(C[0]['s']+0.14,0.34,0.8)
M0=D.get('marks',{}).get('map0',C[0]['s']+0.1)
for i,dt in enumerate((0.0,0.17,0.31,0.5,0.66,0.8,0.98,1.13,1.27)):key(M0+0.06+dt,0.8)          # typing the place name
pop(M0+1.42,0.5,480,0.4);tick(P[2]['wipe'],1.0,p=0.2)
if not C[0].get('hard'):swish(C[0]['e']-0.15,0.28,0.6)
boom(T('b2'),1.0*Q,54,1.3)
whoosh(T('b3')+0.02,0.28,0.8)
pop(T('k1'),0.7,330);whoosh(T('k1')+0.03,0.3,0.7);tick(P[3]['wipe'],0.9)
whoosh(T('d1')+0.03,0.34,0.9,p0=-0.7,p1=0.7)
bell(T('w1')+0.08,(79,84),0.9);tick(P[4]['wipe'],0.9)
swish(T('w2a')+0.05,0.26,0.5);tick(P[5]['wipe'],0.9);pop(T('w2')+0.02,0.5,440)
whoosh(C[1]['s']+0.12,0.34,0.8);tick(P[6]['wipe'],0.9);pop(P[7]['s'],0.45,640);swish(C[1]['e']-0.15,0.28,0.6)
swish(L['s']+0.05,0.26,0.5);tick(P[8]['wipe'],0.9)
for i,r in enumerate(L['rows']):pop(r['at'],0.8,520+i*130,0.3)
swish(T('w6')+0.04,0.3,0.5);tick(P[9]['wipe'],0.9);pop(P[10]['s'],0.45,640)
whoosh(VD+0.04,0.32,0.7);bell(VD+0.32,(72,79,84),1.0)
# ---------------- write ----------------
def wr(name,x):
    x=x[:int(TOTAL*sr)];w=wave.open(name,'w');w.setnchannels(2);w.setsampwidth(3);w.setframerate(sr)
    y=(np.clip(x,-1,1)*8388607).astype(np.int32);b=np.zeros((len(y),2,3),dtype=np.uint8)
    for k in range(3):b[:,:,k]=(y>>(8*k))&255
    w.writeframes(b.tobytes());w.close()
tt=np.arange(N)/sr;music*=np.clip((TOTAL-tt)/1.2,0,1)[:,None];sfx*=np.clip((TOTAL-tt)/0.25,0,1)[:,None]
pk=np.abs(music).max();print('music peak %.3f sfx peak %.3f'%(pk,np.abs(sfx).max()))
wr('music.wav',music/max(1,pk/0.9));wr('sfx.wav',sfx/max(1,np.abs(sfx).max()/0.95))
w=int(sr*1.0);print('music rms per second (dB):',' '.join('%.0f'%(20*np.log10(np.sqrt((music[i:i+w]**2).mean())+1e-6)) for i in range(0,int(TOTAL*sr)-w,w)))
