import numpy as np,wave
from scipy.signal import lfilter
sr=48000;D=1018/30;n=int(sr*D);t=np.arange(n)/sr
rng=np.random.default_rng(7)
def lp(x,fc):
    a=np.exp(-2*np.pi*fc/sr);return lfilter([1-a],[1,-a],x)
def note(f):return 440*2**((f-69)/12)
chords=[[38,57,60,64,65],[34,53,57,60,62],[41,52,57,60,64],[36,52,55,59,62]]
pad=np.zeros(n);ln=D/8
for i in range(8):
    c=chords[i%4];s=i*ln
    env=np.clip((t-s)/1.6,0,1)*np.clip((s+ln+1.4-t)/1.6,0,1);env[t<s]=0
    for j,m in enumerate(c):
        f=note(m)
        for det in(-0.15,0.12):
            ph=2*np.pi*(f*(1+det/100))*t+rng.uniform(0,6)
            pad+=(np.sin(ph)+0.25*np.sin(2*ph)+0.08*np.sin(3*ph))*env*(0.9 if j==0 else 0.45)
pad=lp(lp(pad,1400),1400)
bpm=92;step=60/bpm/2;pl=np.zeros(n);k=0;s=0.0
while s<D-2.4:
    c=chords[int(s/ln)%4];m=[c[2],c[4],c[3],c[4]][k%4]+12;f=note(m)
    i0=int(s*sr);L=int(0.5*sr);tt=np.arange(L)/sr
    if i0+L<n: pl[i0:i0+L]+=np.sin(2*np.pi*f*tt)*np.exp(-tt*9)*(0.5 if k%4 else 0.8)
    s+=step;k+=1
pl=lp(pl,2200)
music=pad/np.abs(pad).max()*0.55+pl/np.abs(pl).max()*0.16
music*=np.clip(t/1.2,0,1)*np.clip((D-t)/1.0,0,1)
sfx=np.zeros(n)
def whoosh(s,d=0.5,g=0.5):
    L=int(d*sr);x=rng.standard_normal(L);tt=np.arange(L)/L
    a=np.exp(-2*np.pi*(400+2600*np.sin(np.pi*tt)**2)/sr);y=np.zeros(L);p=0.0
    for i in range(L):p=a[i]*p+(1-a[i])*x[i];y[i]=p
    y*=np.sin(np.pi*tt)**2;i0=int(s*sr);sfx[i0:i0+L]+=y/np.abs(y).max()*g
def tick(s,g=0.3):
    L=int(0.06*sr);tt=np.arange(L)/sr;y=np.sin(2*np.pi*1500*tt)*np.exp(-tt*90)+0.5*np.sin(2*np.pi*3000*tt)*np.exp(-tt*140)
    i0=int(s*sr);sfx[i0:i0+L]+=y*g
for s in(2.7,12.82,31.62):whoosh(s)
for s in(0.7,6.46,7.6,8.32,10.66,13.7,18.45,21.96,24.46,25.42,32.05):tick(s)
def wr(name,x):
    w=wave.open(name,'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes());w.close()
wr('music.wav',music);wr('sfx.wav',sfx)
