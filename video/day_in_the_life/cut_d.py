# Story cut (worked example: a day in the life): picture segments -> frames/, voice and ambience stems -> voice.wav / amb.wav, segs.json
# usage: SRC=raw.mp4 MODELS=models python3 cut_d.py      Voice lines are levelled per line. The natural sound levels here are set for a mix with no music.
# Picture and sound are listed separately so a line can run as voiceover across other shots.
import os,json,subprocess,wave,shutil,numpy as np
SRC=os.environ.get('SRC','raw.mp4');MODEL=os.environ.get('MODELS','models')+'/bd.rnnn';SR=48000
def run(*a):subprocess.run(list(a),check=True)
# key, (src start, src end)   picture only, 30 fps, 1x
PIC=[('h1',99.20,100.75),('h2',112.60,113.85),
     ('r1',4.00,5.15),('r3',30.30,31.25),('wa',63.50,64.60),('p1',76.15,80.15),('wb',83.90,85.10),
     ('b1',92.82,96.00),('b2',100.80,102.44),('b3',114.00,115.30),('b6',162.91,165.40),
     ('k1',182.90,184.20),('k2',187.70,189.60),('k3',195.20,196.45),('k4',208.55,209.70),('k5',221.20,223.45),
     ('d1',284.00,285.30),('w1',493.40,496.20),
     ('w2a',328.30,329.90),('w2',416.50,418.90),('w3',391.60,394.90),('w5',374.40,378.00),('w6',363.20,365.60),('z1',178.30,179.42)]
# voice: (picture key it starts on, offset in s, src start, src end)
VOICE=[('h1',0.05,130.72,132.02),('b1',0,92.82,96.00),('b2',0,100.80,102.44),('b6',0,162.91,165.40),
       ('k2',0,180.20,182.06),('k3',0.12,200.85,201.80),('k4',0,208.55,209.70),('k5',0.29,221.49,222.90),('z1',0,178.30,179.42)]
# natural sound: (picture key, offset, src start, src end, target rms dBFS). With no music this is the bed, so it sits higher than under a score.
AMB=[('h1',0,99.20,100.75,-36),('h2',0,112.60,113.85,-22),('r1',0,4.00,5.15,-31),('r3',0,30.30,31.25,-29),('wa',0,63.50,64.60,-27),
     ('p1',0,76.15,80.15,-30),('wb',0,83.90,85.10,-27),('b3',0,114.00,115.30,-22),('k1',0,182.90,184.20,-27),('k2',0,187.70,189.60,-31),
     ('k3',0,195.20,196.45,-36),('k5',1.74,222.94,223.45,-30),('d1',0,284.00,285.30,-27),('w1',0,493.40,496.20,-29),
     ('w2a',0,328.30,329.90,-31),('w2',0,416.50,418.90,-31),('w3',0,391.60,394.90,-33),('w5',0,374.40,378.00,-33),('w6',0,363.20,365.60,-31)]
shutil.rmtree('frames',ignore_errors=True);os.makedirs('frames');os.makedirs('tmp',exist_ok=True)
segs=[];f0=0
for k,s,e in PIC:
    shutil.rmtree('tmp/f',ignore_errors=True);os.makedirs('tmp/f')
    run('ffmpeg','-v','error','-y','-ss',f'{s:.3f}','-t',f'{e-s:.3f}','-i',SRC,'-an','-vf','fps=30,setsar=1','-q:v','2','tmp/f/%05d.jpg')
    fs=sorted(os.listdir('tmp/f'))
    for i,f in enumerate(fs):os.replace(f'tmp/f/{f}',f'frames/{f0+i+1:05d}.jpg')
    segs.append({'key':k,'src':[s,e],'f0':f0,'f1':f0+len(fs),'s':round(f0/30,4),'e':round((f0+len(fs))/30,4)});f0+=len(fs)
nf=f0;T={x['key']:x for x in segs};N=int(nf/30*SR)
def grab(s,e,chain,pre=0.9,post=0.25):
    run('ffmpeg','-v','error','-y','-ss',f'{max(0,s-pre):.3f}','-t',f'{e-s+pre+post:.3f}','-i',SRC,'-vn','-af',chain,'-ar',str(SR),'-ac','1','-c:a','pcm_s16le','tmp/a.wav')
    w=wave.open('tmp/a.wav');a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    i=int(min(pre,s)*SR);return a[i:i+int((e-s)*SR)]
def fade(x,a=0.012,r=0.03):
    x=x.copy();na,nr=int(a*SR),int(r*SR);x[:na]*=np.linspace(0,1,na);x[-nr:]*=np.linspace(1,0,nr);return x
def speech_level(x):
    n=int(0.05*SR);r=np.array([np.sqrt((x[i:i+n]**2).mean()+1e-12) for i in range(0,len(x)-n,n//2)]);return 20*np.log10(np.percentile(r,90)+1e-9)
VCH=f"pan=mono|c0=0.5*c0+0.5*c1,highpass=f=85,arnndn=m={MODEL}:mix=0.8,equalizer=f=280:t=q:w=1.0:g=-2,equalizer=f=4200:t=q:w=1.2:g=2.5,equalizer=f=9500:t=h:w=4000:g=1.5,deesser=i=0.25,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=140:makeup=2"
ACH="pan=mono|c0=0.5*c0+0.5*c1,highpass=f=140,lowpass=f=9000"
voice=np.zeros(N,np.float32);amb=np.zeros(N,np.float32);vev=[]
for k,off,s,e in VOICE:
    x=grab(s,e,VCH);lv=speech_level(x);g=float(np.clip(-21-lv,-8,14));x=fade(x*10**(g/20));t0=T[k]['s']+off;i=int(t0*SR);n=min(len(x),N-i);voice[i:i+n]+=x[:n]
    vev.append({'key':k,'t0':round(t0,4),'t1':round(t0+len(x)/SR,4),'src':[s,e],'gain_db':round(g,1)});print(f'voice {k:4s} at {t0:6.2f}s level {lv:6.1f} dB gain {g:+.1f}')
for k,off,s,e,tg in AMB:
    x=grab(s,e,ACH,pre=0.2,post=0.1);lv=20*np.log10(np.sqrt((x**2).mean())+1e-9);g=float(np.clip(tg-lv,-30,12));x=fade(x*10**(g/20),0.05,0.08);i=int((T[k]['s']+off)*SR);n=min(len(x),N-i);amb[i:i+n]+=x[:n]
def wr(p,x):
    w=wave.open(p,'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes());w.close()
wr('voice.wav',voice);wr('amb.wav',amb)
json.dump({'segs':segs,'voice':vev,'nf':nf},open('segs.json','w'),indent=1)
for x in segs:print(f"{x['key']:4s} {x['s']:6.2f} to {x['e']:6.2f}  ({x['e']-x['s']:.2f}s)  src {x['src'][0]:.2f}")
print('frames',nf,'=',round(nf/30,2),'s')
