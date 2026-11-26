# Stereo score + sound design for the sales call montage. Everything is synthesised here (no samples).
import numpy as np,json,wave
from scipy.signal import butter,sosfilt,sosfilt_zi,fftconvolve,lfilter
sr=48000
D=json.load(open('data.json'));TOTAL=D['total']/30.0;N=int(sr*(TOTAL+0.5))
rng=np.random.default_rng(11)
SC={s['key']:s for s in D['sc']}
def wt(k,i):return SC[k]['w'][i][1]
VD=D['vd']
# ---------------- helpers ----------------
def note(m):return 440.0*2**((m-69)/12)
def st(x,p=0.0):
    """mono -> stereo with equal-power pan p in [-1,1]"""
    a=(p+1)*np.pi/4;return np.stack([x*np.cos(a),x*np.sin(a)],1)
def bq(x,kind,fc,order=2,fc2=None):
    if kind=='bp':sos=butter(order,[fc/(sr/2),fc2/(sr/2)],btype='band',output='sos')
    else:sos=butter(order,min(0.99,fc/(sr/2)),btype={'lp':'low','hp':'high'}[kind],output='sos')
    return sosfilt(sos,x,axis=0)
def tvlp(x,fcs,order=2,blk=256):
    """time-varying low-pass: fcs is an array (per sample) of cutoff Hz, processed in blocks keeping filter state"""
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
def fade(x,a=0.005,r=0.02):
    n=len(x);e=np.ones(n);na=int(a*sr);nr=int(r*sr)
    if na>0:e[:na]=np.linspace(0,1,na)
    if nr>0:e[-nr:]*=np.linspace(1,0,nr)
    return x*(e if x.ndim==1 else e[:,None])
def reverb(x,decay=2.4,pre=0.018,lp=5200,hp=180,seed=1):
    r=np.random.default_rng(seed);n=int(decay*sr);t=np.arange(n)/sr
    ir=np.stack([r.standard_normal(n),r.standard_normal(n)],1)*np.exp(-t*6.9/decay)[:,None]
    ir=bq(bq(ir,'lp',lp),'hp',hp);ir[:int(0.004*sr)]*=np.linspace(0,1,int(0.004*sr))[:,None]
    ir/=np.sqrt((ir**2).sum(0)).mean()
    xs=x if x.ndim==2 else st(x)
    out=np.stack([fftconvolve(xs[:,0],ir[:,0]),fftconvolve(xs[:,1],ir[:,1])],1)
    pd=int(pre*sr);out=np.concatenate([np.zeros((pd,2)),out],0);return out
# ---------------- tempo grid fitted to picture ----------------
EV=[(wt('dream',4),2),(SC['take']['s'],2),(SC['three']['s'],2),(SC['street']['s'],2),(SC['follow']['s'],2),(SC['conv']['s'],1.5),(wt('conv',6),1.5),(SC['prob']['s'],1.5),(SC['one']['s'],1.5),(wt('one',12),2),(VD,3),(SC['c_found']['s'],1),(SC['c_ten']['s'],1)]
best=None
for bpm in np.arange(74,84.01,0.1):
    b8=60/bpm/2
    for ph in np.arange(0,b8,0.01):
        c=sum(w*(((t-ph+b8/2)%b8)-b8/2)**2 for t,w in EV)
        if best is None or c<best[0]:best=(c,bpm,ph)
_,BPM,PH=best;BEAT=60/BPM;BAR=4*BEAT
# bar 0 starts so that the end card (VD) falls on a bar line when possible
k=round((VD-PH)/BAR);T0=VD-k*BAR
while T0>0:T0-=BAR
print(f'tempo {BPM:.1f} bpm, phase {PH:.3f}s, bar {BAR:.3f}s, first bar at {T0:.3f}s')
def bt(bar,beat=0.0):return T0+bar*BAR+beat*BEAT
NB=int(np.ceil((TOTAL-T0)/BAR))+1
# ---------------- harmony ----------------
CH=[([50,53,57,64],38),([46,53,58,62],34),([53,57,60,67],41),([52,55,60,67],36)]   # Dm9, Bbmaj, F, C/E   (pad notes, bass note)
MOTIF=[[(0,69,.9),(1.5,65,.6),(3,64,.7)],[(0,62,.8),(1.5,65,.6),(3,69,.75)],[(0,72,.9),(1.5,69,.6),(3,67,.7)],[(0,64,.8),(1.5,67,.6),(3,72,.8)]]
# intensity automation by picture section (0..1)
SEC=[(0,0.35),(SC['ask']['s'],0.18),(SC['c_found']['s'],0.42),(SC['take']['s'],0.62),(SC['c_three']['s'],0.5),(SC['three']['s'],0.72),(SC['c_ten']['s'],0.55),(SC['street']['s'],0.85),(SC['follow']['s'],0.8),(SC['c_org']['s'],0.6),(SC['conv']['s'],0.9),(SC['c_plain']['s'],0.5),(SC['prob']['s'],0.75),(SC['one']['s'],0.8),(wt('one',12),1.0),(VD,1.0),(VD+1.6,0.6)]
tt=np.arange(N)/sr
inten=np.interp(tt,[s for s,_ in SEC],[v for _,v in SEC]);inten=lfilter([1-np.exp(-1/(0.12*sr))],[1,-np.exp(-1/(0.12*sr))],inten)
# ---------------- pad (supersaw through moving low-pass) ----------------
pad=np.zeros((N,2))
for b in range(NB):
    notes,_=CH[b%4];s=bt(b);L=BAR+1.8;n=int(L*sr);t=np.arange(n)/sr
    e=np.clip(t/1.3,0,1)*np.clip((L-t)/1.6,0,1);e=e*e*(3-2*e)
    for m in notes:
        f=note(m)
        for ch in(0,1):
            x=np.zeros(n)
            for d in rng.uniform(-14,14,5):
                ph=rng.uniform(0,1);x+=2*((f*2**(d/1200)*t+ph)%1)-1
            add(pad[:,ch],x*e*0.05,s)
cut=420+1500*inten+260*np.sin(2*np.pi*0.11*tt)
pad=np.stack([tvlp(pad[:,0],cut,order=4),tvlp(pad[:,1],cut,order=4)],1)
pad+=0.5*reverb(pad,decay=3.2,lp=3000,seed=3)[:N]
# ---------------- sub / bass ----------------
bass=np.zeros(N)
for b in range(NB):
    _,m=CH[b%4];f=note(m);s=bt(b);L=BAR;n=int(L*sr);t=np.arange(n)/sr
    e=np.clip(t/0.06,0,1)*np.clip((L-t)/0.25,0,1)
    x=np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*2*f*t)*np.exp(-t*1.2)
    add(bass,np.tanh(x*1.6)*e*0.5,s)
    # syncopated 808 push on the "and" of 3 when intensity is high
    s2=bt(b,2.5);n2=int(1.4*BEAT*sr);t2=np.arange(n2)/sr
    fr=f*2*(1+0.6*np.exp(-t2*30));x2=np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-t2*3.0)
    add(bass,np.tanh(x2*2.0)*0.42*float(np.interp(s2,[s for s,_ in SEC],[v for _,v in SEC])>0.58),s2)
bass=bq(bass,'lp',900)*(0.55+0.45*inten)
# ---------------- felt piano ----------------
def piano(m,vel=0.7,dur=3.2):
    f=note(m);n=int(dur*sr);t=np.arange(n)/sr;x=np.zeros(n);B=0.00035
    for k in range(1,11):
        fk=f*k*np.sqrt(1+B*k*k)
        if fk>9000:break
        x+=np.sin(2*np.pi*fk*t+rng.uniform(0,6.28))*np.exp(-t*(0.9+0.42*k))/k**1.55
    x*=np.clip(t/0.012,0,1);x+=bq(rng.standard_normal(n),'lp',900)*np.exp(-t*90)*0.12
    return bq(x,'lp',1700+2200*vel)*vel
pno=np.zeros((N,2))
for b in range(NB):
    for (beat,m,v) in MOTIF[b%4]:
        s=bt(b,beat)
        if s<SC['c_found']['s']-0.1 or s>VD+0.2:continue
        g=float(np.interp(s,[q for q,_ in SEC],[v2 for _,v2 in SEC]))
        add(pno,st(piano(m,v*(0.55+0.5*g)),rng.uniform(-0.35,0.35)),s,0.16)
pno=pno+0.9*reverb(pno,decay=3.4,lp=4200,seed=5)[:N]
# ---------------- pulse (muted pluck, ping-pong) ----------------
def pluck(f,dur=0.5,bright=0.5):
    n=int(dur*sr);P=int(sr/f);buf=bq(rng.standard_normal(P),'lp',1500+3500*bright);out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%P];buf[i%P]=0.5*(buf[i%P]+buf[(i+1)%P])*0.992
    return out*np.exp(-np.arange(n)/sr*5)
pl=np.zeros((N,2));cache={}
for b in range(NB):
    notes,bm=CH[b%4]
    for e8 in range(8):
        s=bt(b,e8*0.5)
        if s<SC['c_found']['s']-0.05 or s>VD:continue
        m=[bm+24,notes[2]+0,bm+24,notes[1]+12,bm+24,notes[2],notes[3],notes[1]+12][e8]
        if m not in cache:cache[m]=pluck(note(m))
        g=float(np.interp(s,[q for q,_ in SEC],[v for _,v in SEC]))
        add(pl,st(cache[m],-0.5 if e8%2==0 else 0.5),s,0.10*(0.35+0.9*g)*(1.0 if e8%4==0 else 0.7))
dl=int(0.75*BEAT*sr);echo=np.zeros_like(pl);echo[dl:,0]=pl[:-dl,1]*0.42;echo[dl:,1]=pl[:-dl,0]*0.42;pl=bq(pl+echo,'lp',3200)
pl+=0.35*reverb(pl,decay=1.8,lp=3500,seed=7)[:N]
# ---------------- drums ----------------
def kick(g=1.0):
    n=int(0.42*sr);t=np.arange(n)/sr;f=44+78*np.exp(-t*26);x=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*8.5)
    return np.tanh((x+bq(rng.standard_normal(n),'lp',2500)*np.exp(-t*240)*0.25)*1.5)*g
def hat(g=1.0,dec=45):
    n=int(0.09*sr);t=np.arange(n)/sr;return bq(rng.standard_normal(n),'hp',7500)*np.exp(-t*dec)*g
def clap(g=1.0):
    n=int(0.28*sr);t=np.arange(n)/sr;x=np.zeros(n)
    for d in(0,0.010,0.021):
        k=int(d*sr);x[k:]+=rng.standard_normal(n-k)*np.exp(-np.arange(n-k)/sr*(60 if d<0.02 else 22))
    return bq(x,'bp',900,2,3600)*g*0.5
dr=np.zeros((N,2))
for b in range(NB):
    for q in range(16):
        s=bt(b,q*0.25)
        if s<SC['take']['s']-0.02 or s>VD-0.05:continue
        g=float(np.interp(s,[q2 for q2,_ in SEC],[v for _,v in SEC]))
        if q in(0,10) and g>0.45:add(dr,st(kick(0.75)),s,0.5*g)
        if q==8 and g>0.7:add(dr,st(clap(),0.08),s,0.34*g)
        if q%2==0 and g>0.55:add(dr,st(hat(0.5 if q%4 else 0.8),0.25 if q%4 else -0.2),s,0.10*g)
        if q in(7,15) and g>0.75:add(dr,st(hat(0.45,80),0.4),s,0.08*g)
dr+=0.22*reverb(bq(dr,'hp',400),decay=1.1,lp=5000,seed=9)[:N]
music=pad*0.9+st(bass)*0.85+pno+pl+dr
# hook: let the bed breathe in, and pull right back under the "ask" beat
g=np.ones(N);g*=np.clip(tt/0.25,0,1);music*=g[:,None]
# ---------------- sound effects ----------------
sfx=np.zeros((N,2))
def boom(t,g=1.0,f0=62,tail=1.3,p=0.0):
    n=int(tail*sr);x=np.arange(n)/sr;f=f0*np.exp(-x*2.6)+30;y=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-x*3.4)
    th=bq(rng.standard_normal(n),'bp',70,2,420)*np.exp(-x*16)*1.2;ck=bq(rng.standard_normal(n),'bp',1200,2,4200)*np.exp(-x*70)*0.22
    s=st(np.tanh((y+th)*1.4)+ck,p);add(sfx,s,t,g*0.62);add(sfx,reverb(bq(s,'hp',160),decay=1.9,lp=2600,seed=int(t*100)%97+2),t,g*0.16)
def braam(t,g=1.0,root=38,dur=1.25):
    n=int(dur*sr);x=np.arange(n)/sr;y=np.zeros((n,2))
    for m in(root,root+7,root+12):
        for ch in(0,1):
            for d in rng.uniform(-16,16,4):y[:,ch]+=2*((note(m)*2**(d/1200)*x+rng.uniform())%1)-1
    e=np.clip(x/0.05,0,1)*np.exp(-x*2.3);fc=220+1500*np.exp(-x*3.2)
    y=np.stack([tvlp(y[:,0],fc,4),tvlp(y[:,1],fc,4)],1)*e[:,None];add(sfx,np.tanh(y*0.5),t,g*0.2);add(sfx,reverb(y,decay=2.2,lp=2200,seed=31),t,g*0.035)
def whoosh(t_end,dur=0.42,g=1.0,lo=350,hi=5200,p0=-0.7,p1=0.7):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=lo+(hi-lo)*x**2.2;y=tvlp(y,fc,2)-tvlp(y,fc*0.35,2)
    e=x**2.4*np.clip((1-x)/0.05,0,1);p=p0+(p1-p0)*x;a=(p+1)*np.pi/4;add(sfx,np.stack([y*e*np.cos(a),y*e*np.sin(a)],1),t_end-dur,g*0.5)
def swish(t,dur=0.3,g=1.0,p0=0.6,p1=-0.6):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=900+3800*np.sin(np.pi*x)**2;y=tvlp(y,fc,2)-tvlp(y,fc*0.4,2)
    e=np.sin(np.pi*x)**2;p=p0+(p1-p0)*x;a=(p+1)*np.pi/4;add(sfx,np.stack([y*e*np.cos(a),y*e*np.sin(a)],1),t-dur*0.45,g*0.42)
def riser(t_end,dur=1.3,g=1.0):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=250+7000*x**3;y=tvlp(y,fc,2);e=x**3
    f=180*2**(x*2.2);tone=np.sin(2*np.pi*np.cumsum(f)/sr)*x**2*0.35
    add(sfx,np.stack([(y*e+tone)*(0.6+0.4*np.sin(2*np.pi*7*x*x)),(y*e+tone)*(0.6+0.4*np.cos(2*np.pi*7*x*x))],1),t_end-dur,g*0.34)
def flashpop(t,g=1.0):
    n=int(0.5*sr);x=np.arange(n)/sr;y=bq(rng.standard_normal(n),'hp',2500)*np.exp(-x*38)+bq(rng.standard_normal(n),'bp',300,2,1400)*np.exp(-x*20)*0.7
    s=st(y);add(sfx,s,t,g*0.3);add(sfx,reverb(s,decay=1.3,lp=6000,seed=41),t,g*0.07)
def zap(t,g=1.0):
    n=int(0.16*sr);x=np.arange(n)/sr;f=2400*np.exp(-x*26)+160;y=np.sign(np.sin(2*np.pi*np.cumsum(f)/sr))*np.exp(-x*24)
    nz=rng.standard_normal(n);k=24;nz=np.repeat(nz[::k],k)[:n]*np.exp(-x*30)
    add(sfx,st(bq(y*0.5+nz*0.6,'bp',500,2,6500),rng.uniform(-0.4,0.4)),t,g*0.2)
def tick(t,g=1.0,f=2200,p=0.0):
    n=int(0.05*sr);x=np.arange(n)/sr;y=(np.sin(2*np.pi*f*x)+0.4*bq(rng.standard_normal(n),'hp',4000))*np.exp(-x*150);add(sfx,st(y,p),t,g*0.1)
def pop(t,g=1.0,f=520,p=0.0):
    n=int(0.13*sr);x=np.arange(n)/sr;y=np.sin(2*np.pi*np.cumsum(f*(1+0.9*np.exp(-x*60)))/sr)*np.exp(-x*34);add(sfx,st(y,p),t,g*0.2)
def thock(t,g=1.0,p=0.0):
    n=int(0.2*sr);x=np.arange(n)/sr;y=np.sin(2*np.pi*np.cumsum(150*(1+1.3*np.exp(-x*70)))/sr)*np.exp(-x*26)+bq(rng.standard_normal(n),'bp',700,2,2600)*np.exp(-x*85)*0.4
    add(sfx,st(y,p),t,g*0.3)
def bell(t,notes=(81,86),g=1.0):
    for i,m in enumerate(notes):
        n=int(1.6*sr);x=np.arange(n)/sr;f=note(m);y=(np.sin(2*np.pi*f*x)+0.35*np.sin(2*np.pi*2.76*f*x)*np.exp(-x*6)+0.2*np.sin(2*np.pi*5.4*f*x)*np.exp(-x*12))*np.exp(-x*4.2)*np.clip(x/0.004,0,1)
        s=st(y,-0.3+0.6*i);add(sfx,s,t+i*0.085,g*0.085);add(sfx,reverb(s,decay=2.0,lp=7000,seed=51+i),t+i*0.085,g*0.03)
def blip(t,g=1.0):
    for i,f in enumerate((660,990)):
        n=int(0.07*sr);x=np.arange(n)/sr;y=np.sin(2*np.pi*f*x)*np.sin(np.pi*x/0.07)**2;add(sfx,st(y,-0.55),t+i*0.075,g*0.07)
def static(t0,t1,g=1.0):
    n=int((t1-t0)*sr);x=np.arange(n)/n;y=bq(rng.standard_normal(n),'bp',1800,2,7000)*0.5+0.35*np.sin(2*np.pi*50*np.arange(n)/sr)+0.2*np.sin(2*np.pi*100*np.arange(n)/sr)
    e=np.clip(x/0.12,0,1)*np.clip((1-x)/0.1,0,1);add(sfx,np.stack([y*e,np.roll(y,300)*e],1),t0,g*0.045)
# --- hook
boom(0.02,0.7);whoosh(wt('dream',4)-0.02,0.34,0.8);boom(wt('dream',4)-0.03,1.05,70);braam(wt('dream',4)-0.03,0.9);boom(wt('dream',7)-0.03,0.55,56)
# --- ask (negative flash)
zap(SC['ask']['s'],1.0);swish(SC['ask']['s']+0.02,0.3,0.6)
# --- client: found us
blip(SC['c_found']['s']+0.03);swish(SC['c_found']['s']+0.08,0.3,0.5,-0.7,0.2)
tB=wt('c_found',7)-0.16;whoosh(tB+0.02,0.36,0.9,p0=0.8,p1=-0.6);thock(tB+0.06,0.7,0.5)
for i in range(9):tick(tB+0.14+i*0.066+rng.uniform(-0.008,0.008),0.6+0.3*rng.uniform(),2600+rng.uniform(-300,300),0.45)
for i,d in enumerate((0.5,0.6,0.7)):pop(tB+d,0.5,420+i*90,0.5)
tR=wt('c_found',12)+0.12;bell(tR,(81,86),1.0);boom(tR,0.5,60,0.9,0.4)
# --- take
whoosh(SC['take']['s'],0.4,0.9);flashpop(SC['take']['s'],1.0);boom(SC['take']['s'],0.6,58);swish(SC['take']['s']+0.1,0.3,0.5,0.7,-0.6);pop(wt('take',8)-0.02,0.5,640,-0.3)
# --- three videos
blip(SC['c_three']['s']+0.03);swish(SC['c_three']['s']+0.08,0.3,0.45,-0.7,0.2)
for i in range(3):pop(wt('c_three',7)-0.05+i*0.09,0.7,480+i*110,-0.6+i*0.2)
whoosh(SC['three']['s'],0.4,0.9);flashpop(SC['three']['s'],0.9);boom(SC['three']['s']+0.01,0.95,66);braam(SC['three']['s']+0.01,0.5,41,0.9)
zap(SC['test']['s'],0.9)
# --- ten questions
blip(SC['c_ten']['s']+0.03);swish(SC['c_ten']['s']+0.08,0.3,0.45,-0.7,0.2)
t0=wt('c_ten',2)-0.05
for k in range(10):thock(t0+k*0.062+0.12,0.34+0.03*k,-0.5);tick(t0+k*0.062+0.12,0.5,1500+k*130,-0.4)
# --- street wall
whoosh(SC['street']['s'],0.5,1.0,p0=0.8,p1=-0.8);boom(SC['street']['s'],0.8,60);static(SC['street']['s'],SC['street']['e'],1.0);thock(SC['street']['s']+0.03,0.8)
boom(wt('street',6)-0.03,0.7,64);boom(wt('street',7)-0.03,0.9,70);braam(wt('street',6)-0.03,0.6,38,1.3)
riser(SC['street']['e'],0.75,0.9);whoosh(SC['street']['e'],0.3,1.0,300,7000)
# --- follow
flashpop(SC['follow']['s'],1.1);boom(SC['follow']['s'],0.85,62);thock(wt('follow',3)-0.05,0.9,-0.5);swish(wt('follow',3)-0.06,0.26,0.5,-0.8,-0.2)
thock(wt('follow',6)-0.05,0.9,-0.5);swish(wt('follow',6)-0.06,0.26,0.5,-0.8,-0.2);pop(wt('follow',7)-0.02,0.5,600,-0.4)
# --- organic / conversion
blip(SC['c_org']['s']+0.03);swish(SC['c_org']['s']+0.08,0.3,0.45,-0.7,0.2)
whoosh(SC['conv']['s'],0.4,0.9);flashpop(SC['conv']['s'],0.9);boom(SC['conv']['s'],0.55,58)
riser(wt('conv',6)-0.04,0.9,0.7);boom(wt('conv',6)-0.04,1.1,72);braam(wt('conv',6)-0.04,1.0,38,1.3)
# --- plain (three punches)
for i,c in enumerate((SC['c_plain']['s'],wt('c_plain',4)-0.04,wt('c_plain',9)-0.04)):
    zap(c,0.8);boom(c,0.5+0.12*i,56+4*i,0.8)
blip(SC['c_plain']['s']+0.05)
# --- the problem
zap(SC['prob']['s'],0.9);whoosh(SC['prob']['s'],0.36,0.8);boom(SC['prob']['s'],0.6,58)
whoosh(wt('prob',5)-0.04,0.3,0.7);boom(wt('prob',5)-0.04,1.0,68);braam(wt('prob',5)-0.04,0.7,41,1.1);pop(wt('prob',3)+0.25,0.5,700,0.5);pop(wt('prob',9)-0.05,0.4,420,0.6)
# --- number one
whoosh(SC['one']['s'],0.4,0.9);flashpop(SC['one']['s'],0.9);boom(SC['one']['s'],0.55,58);swish(wt('one',7)-0.03,0.3,0.5)
riser(wt('one',12)-0.04,1.35,1.0);boom(wt('one',12)-0.04,1.0,70);boom(wt('one',13)-0.04,1.25,76,1.6);braam(wt('one',12)-0.04,1.1,38,1.5)
# --- end card
riser(VD,0.55,0.8);flashpop(VD,1.2);boom(VD+0.02,1.35,74,2.2);braam(VD+0.02,1.0,38,2.2);swish(VD+0.75+0.45,0.9,0.7,-0.9,0.9);bell(VD+0.62,(74,81,86),0.9)
# ---------------- write ----------------
def wr(name,x):
    x=x[:int(TOTAL*sr)];w=wave.open(name,'w');w.setnchannels(2);w.setsampwidth(3);w.setframerate(sr)
    y=(np.clip(x,-1,1)*8388607).astype(np.int32);b=np.zeros((len(y),2,3),dtype=np.uint8)
    for k in range(3):b[:,:,k]=(y>>(8*k))&255
    w.writeframes(b.tobytes());w.close()
tail=np.clip((TOTAL-tt)/1.1,0,1)[:,None]
music*=tail;sfx*=np.clip((TOTAL-tt)/0.25,0,1)[:,None]
pk=np.abs(music).max();print('music peak',pk,'sfx peak',np.abs(sfx).max())
wr('music.wav',music/max(1,pk/0.9));wr('sfx.wav',sfx/max(1,np.abs(sfx).max()/0.95))
json.dump({'bpm':BPM,'t0':T0,'bar':BAR},open('tempo.json','w'))
