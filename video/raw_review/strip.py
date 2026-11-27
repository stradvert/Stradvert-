# Loudness strip for placing a cut by eye: one character per 5 ms (" .:-=+*#%@" from quiet to loud), a tick every 50 ms.
# Usage: python3 strip.py a48.wav 1263.50:1263.80 [more ranges]
import sys,wave,numpy as np
from scipy.signal import butter,sosfilt
SR=48000;w=wave.open(sys.argv[1]);sos=butter(4,[150/(SR/2),6000/(SR/2)],btype='band',output='sos')
CH=" .:-=+*#%@"
for arg in sys.argv[2:]:
    a,b=map(float,arg.split(':'));w.setpos(int((a-0.1)*SR));x=sosfilt(sos,np.frombuffer(w.readframes(int((b-a+0.2)*SR)),dtype=np.int16).astype(np.float32)/32768)
    s='';ticks=''
    for k in range(int(round((b-a)/0.005))):
        t=a+k*0.005;i=int((t-a+0.1)*SR);seg=x[i-120:i+120];d=20*np.log10(np.sqrt((seg**2).mean())+1e-7)
        s+=CH[int(np.clip((d+42)/32*9,0,9))];ticks+='|' if k%10==0 else ' '
    print(f"{a:.2f}-{b:.2f}\n  {s}\n  {ticks}")
