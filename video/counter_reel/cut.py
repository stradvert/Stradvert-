# Builds the picture (graded frames) and the voice stem from an edit list.
# Usage: python3 cut.py raw.mov a48.wav a48_dn.wav edl.json   (AUDIO_ONLY=1 rebuilds the voice without re-extracting frames)
# edl.json: [{k, a, b, loc, note?, bleep?: [s0,s1], ain?: s, aout?: s, fin?, fout?} | {k, freeze: frame, n: frames, loc}], a and b are source frame numbers.
# Every cut is on a frame boundary that sits in a gap between words; audio gets short fades at each cut.
import json,os,sys,subprocess,wave,numpy as np
from scipy.signal import butter,sosfilt,lfilter
FPS=30;SR=48000
RAW,A48,ADN,EDL=sys.argv[1:5]
E=json.load(open(EDL))
GR={'ts':"eq=contrast=1.05:saturation=1.14:gamma=0.98,unsharp=5:5:0.35",
    'cp':"eq=contrast=1.06:saturation=1.12:gamma=0.99,unsharp=5:5:0.35",
    'dark':"hqdn3d=2:2:4:4,eq=gamma=1.42:contrast=1.04:saturation=1.10:brightness=0.015,unsharp=5:5:0.25"}
DNMIX={'ts':0.55,'cp':0.35,'dark':0.6}
def rd(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
O=rd(A48);Dn=rd(ADN)[480:];n=min(len(O),len(Dn));O=O[:n];Dn=Dn[:n]   # arnndn output runs 10 ms late: line it up before blending
os.makedirs('frames',exist_ok=True)
fi=1;voice=[];segs=[];t0=0
for e in E:
    if 'freeze' in e:
        src=f"frames/{fi-1:05d}.jpg"
        for j in range(e['n']):
            if not os.environ.get('AUDIO_ONLY') and not os.path.exists(f"frames/{fi:05d}.jpg"):os.link(src,f"frames/{fi:05d}.jpg")
            fi+=1
        segs.append({**e,'t0':t0,'t1':t0+e['n']/FPS,'f0':fi-e['n']});t0+=e['n']/FPS;continue
    a,b=e['a'],e['b'];nf=b-a;ta=a/FPS;tb=b/FPS
    if os.environ.get('AUDIO_ONLY'):fi+=nf
    else:
     tmp=f"tmp_{e['k']}";os.makedirs(tmp,exist_ok=True)
     subprocess.run(['ffmpeg','-v','error','-y','-ss',f"{ta-0.5/FPS:.4f}",'-i',RAW,'-frames:v',str(nf),'-vf',GR[e['loc']]+",format=yuvj420p",'-q:v','2',f"{tmp}/%05d.jpg"],check=True)
     got=sorted(os.listdir(tmp));assert len(got)==nf,(e['k'],len(got),nf)
     for g in got:os.replace(f"{tmp}/{g}",f"frames/{fi:05d}.jpg");fi+=1
     os.rmdir(tmp)
    # audio: blend of original and denoised, cut to the frame-aligned span
    i0=int(round(ta*SR));te=max(tb,e.get('aout',tb));i1=i0+int(round((te-ta)*SR))
    m=DNMIX[e['loc']];x=(1-m)*O[i0:i1]+m*Dn[i0:i1]
    if 'bleep' in e:
        s0,s1=e['bleep'];j0=int(s0*SR)-i0;j1=int(s1*SR)-i0
        ref=np.sqrt(np.mean(x[max(0,j0-int(0.4*SR)):j0]**2))
        tt=np.arange(j1-j0)/SR;tone=np.sin(2*np.pi*1000*tt)*ref*1.6
        f=np.minimum(1,np.minimum(tt,tt[::-1])/0.004);x[j0:j1]=tone*f
    fin=int(e.get('fin',0.010)*SR);fout=int(e.get('fout',0.012)*SR)
    g=np.ones(len(x),np.float32);j0=max(0,int(round((e.get('ain',ta)-ta)*SR)))   # ain: audio starts a few ms after the picture cut
    g[:j0]=0;g[j0:j0+fin]=np.linspace(0,1,fin)**1.5
    end=len(x)
    g[end-fout:end]=np.minimum(g[end-fout:end],np.linspace(1,0,fout)**1.5)
    voice.append((int(round(t0*SR)),x*g))
    segs.append({**e,'t0':t0,'t1':t0+nf/FPS,'f0':fi-nf});t0+=nf/FPS
V=np.zeros(int(round(t0*SR))+SR,np.float32)
for p,x in voice:V[p:p+len(x)]+=x
V=V[:int(round(t0*SR))]
w=wave.open('voice_raw.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(V,-1,1)*32767).astype(np.int16).tobytes());w.close()
json.dump(segs,open('segs_out.json','w'),indent=0)
print('frames',fi-1,'dur',round(t0,3),'audio',round(len(V)/SR,3))
