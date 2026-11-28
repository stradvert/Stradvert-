# Score and sound design for a brand trip reel: lo-fi groove, tape stop into the drip, a half-time phased trip, the groove back for the call to action. Everything synthesised (no samples). Writes music.wav and sfx.wav (float, stereo).
import json,sys,numpy as np,soundfile as sf
sys.path.insert(0,'/home/user/Stradvert-/video/counter_reel')
from synth import *
D=json.load(open('data.json'));T=D['T'];WT=D['WT'];TOT=D['total']/30.0;N=int(sr*(TOT+1.5))
def tvlp2(x,fcs,order=2):
    return np.stack([tvlp(np.ascontiguousarray(x[:,c]),fcs,order) for c in (0,1)],1) if x.ndim==2 else tvlp(x,fcs,order)
music=np.zeros((N,2));sfx=np.zeros((N,2));R=np.random.default_rng(7)
BPM=92;B=60/BPM
def env_ad(n,a=0.005,d=0.3):
    t=np.arange(n)/sr;return np.clip(t/a,0,1)*np.exp(-t/d)
def ep(m,dur=1.2,vel=0.6):                      # electric piano: soft bell partials, tremolo
    n=int((dur+1.0)*sr);t=np.arange(n)/sr;f=note(m)
    y=(np.sin(2*np.pi*f*t)+0.32*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)+0.08*np.sin(2*np.pi*3.01*f*t)*np.exp(-t*6))
    e=np.clip(t/0.004,0,1)*np.exp(-t*1.1);e[int(dur*sr):]*=np.exp(-(t[int(dur*sr):]-dur)*9)
    return y*e*(1+0.18*np.sin(2*np.pi*4.6*t))*vel*0.16
def hat(g=1.0,dec=0.035):
    n=int(0.12*sr);t=np.arange(n)/sr;return bq(R.standard_normal(n),'hp',7000)*np.exp(-t/dec)*g*0.22
def sub(m,dur,g=1.0):
    n=int(dur*sr);t=np.arange(n)/sr;y=np.tanh(1.6*np.sin(2*np.pi*note(m)*t))*np.clip(t/0.01,0,1)*np.clip((dur-t)/0.06,0,1);return y*g*0.32
def pad(notes,dur,g=1.0,ph=0.35):            # detuned saw pad with a swept band (phaser feel)
    n=int(dur*sr);t=np.arange(n)/sr;y=np.zeros((n,2))
    for j,m in enumerate(notes):
        for d,p in((-9,-.7),(0,0),(8,.7)):
            s=saw(np.full(n,note(m)*2**(d/1200))*(1+0.004*np.sin(2*np.pi*0.7*t+j)),t,18);y+=st(s,p)
    fc=900+700*np.sin(2*np.pi*ph*t);y=tvlp2(y,fc,2)*0.5+y*0.04
    e=np.clip(t/0.5,0,1)*np.clip((dur-t)/0.4,0,1);return y*e[:,None]*g*0.05
def crackle(dur,g=1.0):
    n=int(dur*sr);y=bq(R.standard_normal(n),'bp',1500,2,6000)*0.02
    for i in R.integers(0,n,int(dur*14)):m=min(n-i,int(0.002*sr));y[i:i+m]+=R.uniform(-1,1)*0.5*np.exp(-np.arange(m)/sr*2500)
    return st(y,0.1)*g
CH=[(57,[69,72,76,79]),(53,[69,72,76,79]),(48,[67,71,74,76]),(55,[67,71,74,78])]   # Am9, Fmaj9, Cmaj9, G6
def groove(t0,t1,bright=1.0,start_bar=0):
    for q in range(int((t1-t0)/(B/2))+1):
        tb=t0+q*B/2
        if tb>=t1-0.02:break
        s8=q%8;bar=start_bar+q//8;root,ch=CH[bar%4];sw=0.04 if q%2 else 0
        if s8 in(0,5):add(music,st(kick(0.9 if s8==0 else 0.65)),tb,0.5)
        if s8 in(2,6):add(music,st(clap(0.8),0.05),tb+0.01,0.38)
        add(music,st(hat(0.9 if q%2==0 else 0.55),0.3),tb+sw,0.5*bright)
        if s8 in(0,3,5):add(music,st(bass(root-12,B*(1.2 if s8==0 else 0.7),0.7),0),tb,0.55)
        if s8==0:
            for i,m in enumerate(ch):add(music,st(ep(m,B*3.6,0.55),-0.4+0.27*i),tb+0.012*i,0.9*bright)
        if s8==4 and bar%2==1:add(music,st(ep(ch[-1]+12,B*0.8,0.35),0.5),tb+sw,0.6*bright)
def tapestop(buf,t0,t1):
    i0,i1=int(t0*sr),int(t1*sr);seg=buf[i0:i1].copy();n=i1-i0;rate=np.linspace(1,0.05,n)**1.3;pos=np.cumsum(rate)
    pos=np.clip(pos,0,n-1);out=np.stack([np.interp(pos,np.arange(n),seg[:,c]) for c in(0,1)],1)*np.linspace(1,0,n)[:,None]**0.6
    buf[i0:i1]=out;buf[i1:]*=0
# ---- music ----
tA0=0.0;tA1=D['honey']['s'];tR=D['honey']['out'];tB1=T['bees'][1];tC0=T['jars'][0];END=D['end']['s']
groove(tA0,tA1+0.6,1.0)
add(music,crackle(TOT),0,0.8)
m1=music.copy();music[:]=0
# intro: low-passed until "Is it strong?" opens it
i_open=int(T['strong'][0]*sr);fcs=np.concatenate([np.full(i_open,650),np.linspace(650,16000,int(0.35*sr)),np.full(len(m1),16000)])[:len(m1)]
m1[:int(tA1*sr)+int(0.6*sr)]=tvlp2(m1[:int(tA1*sr)+int(0.6*sr)],fcs[:int(tA1*sr)+int(0.6*sr)],2)
tapestop(m1,tA1,tA1+0.5);music+=m1
# trip: sub swell, phaser pad, half-time drums, wobbly arpeggio
add(music,sub(45,tR-tA1+0.5,0.8),tA1+0.1,0.9)
add(music,pad([57,64,67,72],tB1-tR+0.6,1.4,0.55),tR-0.15,1.0)
add(music,sub(45,tB1-tR,0.9),tR,0.8)
for q in range(int((tB1-tR)/(B/2))+1):
    tb=tR+0.08+q*B/2
    if tb>tB1:break
    s8=q%8
    if s8==0:add(music,st(kick(1.0)),tb,0.55)
    if s8==4:add(music,reverb(st(clap(0.9)),1.4)[:int(0.9*sr)],tb,0.3)
    add(music,st(hat(0.5),(-1)**q*0.5),tb,0.35)
    m=[69,72,76,79,81,79,76,72][q%8];x=pizz(m,0.6)*(1+0.0*q);add(music,st(x,(-1)**q*0.6),tb,0.35);add(music,st(x,-(-1)**q*0.6),tb+B*0.75,0.15)
groove(tC0,TOT+0.5,1.1,start_bar=0)
# end: button chord
for i,m in enumerate([57,64,69,72,76]):add(music,st(ep(m,1.6,0.6),-0.5+0.25*i),END+0.02+0.01*i,1.1)
add(music,st(kick(1.0)),END+0.02,0.5)
fade=np.ones(N);fe=int((TOT-0.35)*sr);fade[fe:]=np.linspace(1,0,N-fe)**1.5;music*=fade[:,None]
# ---- sound effects ----
def ting():return bell((96,103),1.0)
def shimmer(dur,g=1.0):
    n=int(dur*sr);t=np.arange(n)/sr;y=np.zeros(n)
    for k in range(14):f=R.uniform(2500,7000);ph=R.uniform(0,6);y+=np.sin(2*np.pi*f*t+ph)*np.clip(np.sin(np.pi*(t/dur*R.uniform(1,3)+R.random())),0,1)**8
    return st(y*np.clip(t/0.05,0,1)*np.clip((dur-t)/0.1,0,1)*0.03*g,0.2)
def thump(g=1.0):
    n=int(0.45*sr);t=np.arange(n)/sr;lo=np.sin(2*np.pi*np.cumsum(70*np.exp(-t*9)+45)/sr)*np.exp(-t*9)
    return st(lo*0.7+np.concatenate([stamp(1.0),np.zeros(max(0,n-len(stamp(1.0))))])[:n]*0.6,0)*g
def buzzfx(dur,p0,p1,g=1.0):
    n=int(dur*sr);t=np.arange(n)/sr;f=210*(1+0.03*np.sin(2*np.pi*31*t))*(1+0.06*np.sin(2*np.pi*3*t));y=saw(f,t,30)
    y=bq(y,'bp',350,2,3200)*np.clip(t/0.15,0,1)*np.clip((dur-t)/0.25,0,1)*(0.6+0.4*np.sin(2*np.pi*7*t)**2);pan=np.linspace(p0,p1,n)
    a=(pan+1)*np.pi/4;return np.stack([y*np.cos(a),y*np.sin(a)],1)*g*0.09
def goo(dur,g=1.0):
    n=int(dur*sr);t=np.arange(n)/sr;y=bq(R.standard_normal(n),'lp',420)*0.5*np.clip(t/0.2,0,1)
    for k in range(int(dur*9)):
        s=int(R.uniform(0,dur-0.08)*sr);m=int(0.07*sr);tt=np.arange(m)/sr;f=R.uniform(260,620)*np.exp(-tt*12);y[s:s+m]+=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*40)*0.5
    return st(y*g*0.5,0)
def zap(g=1.0):
    n=int(0.09*sr);t=np.arange(n)/sr;f=np.where(t<0.03,1800,np.where(t<0.06,600,2600));y=np.sign(np.sin(2*np.pi*np.cumsum(f)/sr))*np.exp(-t*25)
    return st(bq(y,'bp',400,2,6000)*g*0.12,0)
def tick():return st(block(3200,0.5),0.3)
add(sfx,whoosh(0.3,0.6),-0.05,0.5)
gw=WT['gold'];add(sfx,ting(),gw[4]-0.02,0.9);add(sfx,shimmer(0.8),0.25,1.0)
for w in D['whips']:add(sfx,whoosh(0.32,0.9),w-0.3,0.9)
for p in D['pulse']:add(sfx,zap(1.0),p['t'],0.8);add(sfx,shimmer(0.5,0.8),p['t'],1)
for k in D['kal']:add(sfx,zap(1.2),k[0],1.0)
for s in D['stamps']:add(sfx,thump(1.0),s['s']+0.02,0.9)
for s in D['stickers']:add(sfx,st(pop(0.9,620),0.2),s['s'],0.8)
for b in D['bursts']:add(sfx,shimmer(0.9,1.6),b['t']-0.05,1);add(sfx,bell((91,98),0.8),b['t'],0.5)
for b in D['bees']:add(sfx,buzzfx(b['e']-b['s'],-0.9*b['dir'],0.9*b['dir'],1.0+0.4*(b['n']>1)),b['s'],1)
tm=D['timer'];k=tm['s']+0.1
while k<tm['e']-0.05:add(sfx,tick(),k,0.7);k+=0.25
h=D['honey'];add(sfx,goo(h['full']-h['s']+0.35),h['s'],1.0);add(sfx,st(kick(1.0)),h['full'],0.5);add(sfx,crash(0.6,1.4),h['full'],0.35)
add(sfx,riser(0.45,1.2),h['out']-0.2,0.8);add(sfx,whoosh(0.4,1.0),h['out'],0.9)
u=D['url'];L=len(u['text'])
for i in range(L):add(sfx,st(block(2400+200*(i%3),0.35),0.2),u['s']+0.08+0.45*i/L,0.55)
add(sfx,whoosh(0.35,0.8),END-0.3,0.8);add(sfx,bell((88,95),1.0),END+0.05,0.8)
sf.write('music.wav',(music[:int(TOT*sr)]*0.7).astype(np.float32),sr,subtype='FLOAT');sf.write('sfx.wav',(sfx[:int(TOT*sr)]*0.6).astype(np.float32),sr,subtype='FLOAT')
print('music peak',round(float(np.abs(music).max()),3),'sfx peak',round(float(np.abs(sfx).max()),3))
