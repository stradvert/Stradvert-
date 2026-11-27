# Instruments and sound effects shared by snd.py and snd_cues.py. Everything is synthesised (no samples, no licences).
import numpy as np
from scipy.signal import butter,sosfilt,sosfilt_zi,fftconvolve
sr=48000;rng=np.random.default_rng(11)
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
    if x.ndim==1 and buf.ndim==2:x=st(x)
    if i<0:x=x[-i:];i=0
    n=min(len(x),len(buf)-i)
    if n>0:buf[i:i+n]+=x[:n]*g
def reverb(x,decay=1.4,pre=0.012,lp=4800,hp=220,seed=1):
    r=np.random.default_rng(seed);n=int(decay*sr);t=np.arange(n)/sr
    ir=np.stack([r.standard_normal(n),r.standard_normal(n)],1)*np.exp(-t*6.9/decay)[:,None]
    ir=bq(bq(ir,'lp',lp),'hp',hp);ir[:int(0.004*sr)]*=np.linspace(0,1,int(0.004*sr))[:,None];ir/=np.sqrt((ir**2).sum(0)).mean()
    xs=x if x.ndim==2 else st(x);out=np.stack([fftconvolve(xs[:,0],ir[:,0]),fftconvolve(xs[:,1],ir[:,1])],1)
    return np.concatenate([np.zeros((int(pre*sr),2)),out],0)
def saw(f,t,nh=14):
    y=np.zeros_like(t)
    for k in range(1,nh+1):
        if np.max(f)*k>sr*0.45:break
        y+=np.sin(2*np.pi*k*np.cumsum(f)/sr)/k
    return y
# ---------------- instruments ----------------
def pizz(m,vel=0.7):
    f=note(m);n=int(0.5*sr);P=max(2,int(sr/f));buf=bq(rng.standard_normal(P),'lp',2600);out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%P];buf[i%P]=0.5*(buf[i%P]+buf[(i+1)%P])*0.985
    t=np.arange(n)/sr;out=out*np.exp(-t*9)
    return bq(out,'bp',f*0.8,2,min(5000,f*9))*vel*1.6
def tuba(m,dur=0.4,vel=0.8):
    n=int((dur+0.12)*sr);t=np.arange(n)/sr;f=note(m)*2**((-40*np.exp(-t*30))/1200)
    x=saw(f,t,10);env=np.clip(t/0.03,0,1)*np.exp(-t*2.2)*np.clip((dur+0.12-t)/0.1,0,1)
    fc=250+900*np.exp(-t*9)+150;y=tvlp(x*env,fc,2)
    return np.tanh(y*2.2)*vel*0.7
def reed(m,dur=0.2,vel=0.6):
    n=int((dur+0.08)*sr);t=np.arange(n)/sr;vib=np.where(t>0.12,1,0)*12*np.sin(2*np.pi*5.6*t)
    f=note(m)*2**(vib/1200);ph=2*np.pi*np.cumsum(f)/sr
    x=np.sin(ph)+0.5*np.sin(3*ph)+0.22*np.sin(5*ph)+0.12*np.sin(7*ph)+0.18*np.sin(2*ph)
    env=np.clip(t/0.012,0,1)*np.clip((dur+0.08-t)/0.05,0,1)*(0.85+0.15*np.exp(-t*20))
    return bq(x*env,'lp',2600)*vel*0.45
def block(f=1000,g=1.0):
    n=int(0.09*sr);t=np.arange(n)/sr;x=np.sin(2*np.pi*f*t)*np.exp(-t*60)+0.6*np.sin(2*np.pi*f*2.71*t)*np.exp(-t*110)+0.3*bq(rng.standard_normal(n),'bp',1500,2,6000)*np.exp(-t*300)
    return x*g*0.5
def kick(g=1.0):
    n=int(0.34*sr);t=np.arange(n)/sr;f=46+80*np.exp(-t*32);x=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*9)
    return bq(np.tanh((x+bq(rng.standard_normal(n),'lp',2000)*np.exp(-t*240)*0.25)*1.4),'lp',2600)*g
def clap(g=1.0):
    n=int(0.25*sr);t=np.arange(n)/sr;nz=bq(rng.standard_normal(n),'bp',900,2,5000);e=np.zeros(n)
    for d in(0,0.011,0.022):e+=np.exp(-np.clip(t-d,0,None)*140)*(t>=d)
    e+=0.5*np.exp(-t*22)*(t>0.03);return nz*e*g*0.6
def shaker(g=1.0,dec=60):
    n=int(0.08*sr);t=np.arange(n)/sr;return bq(rng.standard_normal(n),'hp',6500)*np.clip(t/0.004,0,1)*np.exp(-t*dec)*g
def marimba(m,vel=0.6):
    f=note(m);n=int(0.6*sr);t=np.arange(n)/sr
    x=np.sin(2*np.pi*f*t)*np.exp(-t*7)+0.35*np.sin(2*np.pi*4*f*t)*np.exp(-t*28)+0.1*np.sin(2*np.pi*10*f*t)*np.exp(-t*60)
    return x*np.clip(t/0.002,0,1)*vel*0.55
def bass(m,dur=0.3,vel=0.8):
    f=note(m);n=int((dur+0.1)*sr);t=np.arange(n)/sr
    x=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)*np.exp(-t*6)+0.15*saw(np.full(n,f),t,6)*np.exp(-t*12)
    env=np.clip(t/0.006,0,1)*np.exp(-t*3)*np.clip((dur+0.1-t)/0.06,0,1)
    return np.tanh(x*env*1.5)*vel*0.75
def whistle(m,dur=0.3,vel=0.5):
    n=int((dur+0.1)*sr);t=np.arange(n)/sr;f=note(m)*2**((18*np.sin(2*np.pi*6*t)*np.clip(t/0.15,0,1)-60*np.exp(-t*40))/1200)
    x=np.sin(2*np.pi*np.cumsum(f)/sr)+0.05*bq(rng.standard_normal(n),'bp',note(m)*0.9,2,note(m)*1.1)
    env=np.clip(t/0.03,0,1)*np.clip((dur+0.1-t)/0.08,0,1);return x*env*vel*0.35
# ---------------- sound effects ----------------
def buzzer(g=1.0):
    n=int(0.42*sr);t=np.arange(n)/sr;drift=1-0.035*t/0.42
    x=np.sign(np.sin(2*np.pi*150*drift*t))+0.8*np.sign(np.sin(2*np.pi*156*drift*t))+0.4*np.sin(2*np.pi*300*drift*t)
    env=np.clip(t/0.008,0,1)*np.clip((0.42-t)/0.03,0,1);y=bq(np.tanh(x*env*0.8),'lp',2600);return bq(y,'hp',90)*g*0.42
def stamp(g=1.0):
    n=int(0.4*sr);t=np.arange(n)/sr;f=70*np.exp(-t*18)+42;b=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*12)
    s=bq(rng.standard_normal(n),'bp',800,2,5200)*np.exp(-t*80);return np.tanh((b*1.2+s*0.7)*1.3)*g*0.6
def scratch(g=1.0,dur=0.16):
    n=int(1.0*sr);t=np.arange(n)/sr;src=saw(np.full(n,190.0),t,20)*0.5+bq(rng.standard_normal(n),'bp',400,2,3500)*0.8
    src=bq(src,'bp',250,2,4000);m=int(dur*sr);u=np.arange(m)/m
    pos=(0.25+0.11*np.sin(np.pi*u)**1.6-0.06*np.sin(2*np.pi*u))*sr;pos=np.clip(pos,0,n-2);i=pos.astype(int);fr=pos-i
    y=src[i]*(1-fr)+src[i+1]*fr;y*=np.sin(np.pi*u)**0.5;return y*g*0.8
def whoosh(dur=0.36,g=1.0,lo=350,hi=5200):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=lo+(hi-lo)*x**2.2;y=tvlp(y,fc,2)-tvlp(y,fc*0.35,2)
    e=x**2.2*np.clip((1-x)/0.06,0,1);p=-0.6+1.2*x;a=(p+1)*np.pi/4;return np.stack([y*e*np.cos(a),y*e*np.sin(a)],1)*g*0.4
def pop(g=1.0,f=560):
    n=int(0.13*sr);x=np.arange(n)/sr;return np.sin(2*np.pi*np.cumsum(f*(1+0.9*np.exp(-x*60)))/sr)*np.exp(-x*34)*g*0.22
def boing(g=1.0):
    n=int(0.35*sr);t=np.arange(n)/sr;f=330*(1+0.22*np.sin(2*np.pi*13*t)*np.exp(-t*7))*(1+0.4*np.exp(-t*30));return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*8)*g*0.22
def drumroll(t0,t1,g=1.0,duck=None):
    n=int((t1-t0+0.2)*sr);y=np.zeros(n);step=1/22.0;k=0;tt=0.0
    while tt<t1-t0:
        q=tt/(t1-t0);v=(0.22+0.78*q**1.6)*(0.85+0.3*rng.random())*(1.0 if k%2==0 else 0.8)
        if duck:a_=tt+t0;v*=1-0.62*np.clip((a_-duck[0])/0.08,0,1)*np.clip((duck[1]-a_)/0.06,0,1)    # dips under his answer
        m=int(0.06*sr);u=np.arange(m)/sr;h=bq(rng.standard_normal(m),'bp',1400,2,8000)*np.exp(-u*55)+0.5*np.sin(2*np.pi*185*u)*np.exp(-u*70)
        i=int(tt*sr);y[i:i+m]+=h[:max(0,min(m,n-i))]*v;tt+=step*(1+0.03*(rng.random()-0.5));k+=1
    return y*g*0.5
def trombone(t0,g=1.0):
    out=np.zeros(int(1.4*sr));tt=0.0
    for m,d,last in((58,0.19,0),(57,0.19,0),(56,0.19,0),(55,0.5,1)):
        n=int((d+0.06)*sr);t=np.arange(n)/sr;cents=-25*np.exp(-t*40)+(45*np.sin(2*np.pi*6.5*t)*np.clip((t-0.08)/0.1,0,1) if last else -30*np.clip((t-d+0.08)/0.08,0,1))
        f=note(m)*2**(cents/1200);x=saw(f,t,12)
        env=np.clip(t/0.025,0,1)*np.clip((d+0.06-t)/0.06,0,1)
        wah=500+1500*(0.5+0.5*np.sin(2*np.pi*(6.5 if last else 2.2)*t-np.pi/2))*np.clip(t/0.04,0,1);y=tvlp(x*env,wah,2)
        i=int(tt*sr);out[i:i+n]+=np.tanh(y*1.6)[:len(out)-i];tt+=d
    return out*g*0.55
def choir(notes,dur,g=1.0,att=1.2,seed=3,pw=2.0):
    r=np.random.default_rng(seed);n=int(dur*sr);t=np.arange(n)/sr;y=np.zeros((n,2))
    for j,m in enumerate(notes):
        for v in range(3):
            vib=14*np.sin(2*np.pi*(5.0+0.4*r.random())*t+r.random()*6)+r.uniform(-9,9);f=note(m)*2**(vib/1200)
            src=saw(f,t,30)
            fm=bq(src,'bp',600,2,1000)*1.0+bq(src,'bp',1000,2,1350)*0.6+bq(src,'bp',2300,2,3000)*0.25
            p=-0.6+1.2*((j*3+v)/(len(notes)*3-1+1e-9));y+=st(fm,p)
    env=np.clip(t/att,0,1)**pw;return y*env[:,None]*g*0.06
def crash(g=1.0,dec=1.6):
    n=int(dec*1.4*sr);t=np.arange(n)/sr;x=bq(rng.standard_normal(n),'hp',3800)*np.exp(-t*3.2/dec)*(1+0.5*np.exp(-t*30))
    met=np.sign(np.sin(2*np.pi*540*t))*np.sign(np.sin(2*np.pi*813*t))*np.sign(np.sin(2*np.pi*1170*t));x+=0.2*bq(met,'hp',3000)*np.exp(-t*5)
    return st(x,0.15)*g*0.35
def popper(g=1.0):
    n=int(0.5*sr);t=np.arange(n)/sr;x=bq(rng.standard_normal(n),'bp',800,2,6000)*np.exp(-t*90)*1.2
    for k in range(26):
        d=rng.uniform(0.04,0.45);m=int(0.006*sr);i=int(d*sr);x[i:i+m]+=rng.uniform(-1,1)*bq(rng.standard_normal(m),'hp',3000)*np.exp(-np.arange(m)/sr*500)*0.6
    return x*g*0.4
def bell(notes=(88,93),g=1.0):
    out=np.zeros((int(1.8*sr),2))
    for i,m in enumerate(notes):
        n=int(1.4*sr);x=np.arange(n)/sr;f=note(m);y=(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*2.76*f*x)*np.exp(-x*6))*np.exp(-x*4)*np.clip(x/0.003,0,1)
        add(out,st(y,-0.3+0.6*i),i*0.07,0.18)
    return out+0.25*reverb(out,1.6,lp=7000,seed=5)[:len(out)]
def riser(dur,g=1.0):
    n=int(dur*sr);x=np.arange(n)/n;y=rng.standard_normal(n);fc=300+7000*x**2.5;y=tvlp(y,fc,2)-tvlp(y,fc*0.4,2);return y*x**2*g*0.3
