# Transcribe every cut piece on its own (padded with silence) and the whole track, to prove no word is clipped.
# Usage: python3 cutcheck.py voice.wav segs_out.json   (also works on the final stereo mix)
# A clipped edge shows up as a missing or garbled first or last word. Very short pieces (one word) can read wrong on their own: check them in the full pass.
import json,os,sys,wave,numpy as np
os.environ['HF_HUB_DISABLE_XET']='1'
from faster_whisper import WhisperModel
from scipy.signal import resample_poly
import soundfile as sf
V,SR=sf.read(sys.argv[1] if len(sys.argv)>1 else 'voice_raw.wav',dtype='float32')
if V.ndim>1:V=V.mean(1)
assert SR==48000
V16=resample_poly(V,1,3).astype(np.float32)
S=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'segs_out.json'))
m=WhisperModel('medium.en',device='cpu',compute_type='int8',cpu_threads=4)
def tr(x,off=0.0):
    segs,_=m.transcribe(x,language='en',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,temperature=0)
    return [(x_.word.strip(),round(x_.start+off,3),round(x_.end+off,3),round(x_.probability,2)) for s in segs for x_ in s.words]
out={'pieces':{},'full':[]}
for s in S:
    if 'freeze' in s:continue
    a=int(s['t0']*16000);b=int(s['t1']*16000)
    x=np.concatenate([np.zeros(4800,np.float32),V16[a:b],np.zeros(4800,np.float32)])
    ws=tr(x,s['t0']-0.3);out['pieces'][s['k']]=ws
    print(f"{s['k']:5s} {s['t0']:6.2f}-{s['t1']:6.2f} | "+' '.join(f"{w_[0]}({w_[3]})" for w_ in ws)+f"   [want: {s.get('note','')}]",flush=True)
out['full']=tr(V16)
json.dump(out,open('cutcheck_words.json','w'),indent=0)
print('FULL:',' '.join(w_[0] for w_ in out['full']))
