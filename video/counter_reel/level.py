# Per-line levelling: every line (host or guest) is brought to the same speech level, then EQ and gentle compression.
# Usage: python3 level.py voice_raw.wav lines.json   -> voice.wav
import json,sys,wave,subprocess,numpy as np
from scipy.signal import butter,sosfilt
SR=48000
w=wave.open(sys.argv[1]);V=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
L=[tuple(x) for x in json.load(open(sys.argv[2]))]   # [[t0, t1, who]]: H host, G guest, L laugh (gain capped), - no voice
B=sosfilt(butter(4,[150/(SR/2),6000/(SR/2)],btype='band',output='sos'),V)
TARGET=-19.0
g_db=[]
for a,b,who in L:
    x=B[int(a*SR):int(b*SR)]
    if who=='-' or len(x)<960:g_db.append(0.0);continue
    fr=x[:len(x)//960*960].reshape(-1,960);r=np.sqrt((fr**2).mean(1))+1e-7
    act=np.sort(r)[int(len(r)*0.6):]               # loudest 40 percent of 20 ms frames = the speech
    lev=20*np.log10(np.sqrt((act**2).mean()));floor=20*np.log10(np.percentile(r,15))
    g=float(np.clip(TARGET-lev,-8,13 if who!='L' else 3))
    g_db.append(g);print(f"{a:6.2f}-{b:6.2f} {who} speech {lev:6.1f} dB floor {floor:6.1f} dB  gain {g:+5.1f} dB -> floor {floor+g:6.1f}")
gain=np.zeros(len(V),np.float32)
for (a,b,who),g in zip(L,g_db):gain[int(a*SR):int(b*SR)]=g
gain[int(min(L[-1][1],len(V)/SR)*SR):]=g_db[-1]
k=int(0.04*SR);gain=np.convolve(np.pad(gain,(k,k),mode='edge'),np.ones(k)/k,mode='same')[k:-k]   # 40 ms ramps between lines
Y=V*10**(gain/20)
w=wave.open('voice_lev.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(Y,-1,1)*32767).astype(np.int16).tobytes());w.close()
subprocess.run(['ffmpeg','-v','error','-y','-i','voice_lev.wav','-af',
 'highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,acompressor=threshold=-24dB:ratio=2.6:attack=5:release=110:makeup=2,alimiter=limit=0.9:level=false',
 '-ar','48000','voice.wav'],check=True)
print('voice.wav written')
