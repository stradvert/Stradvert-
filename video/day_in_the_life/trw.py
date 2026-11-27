# Word transcript with confidence per word. usage: python3 trw.py audio_16k_mono.wav words.json
import os,json,sys,wave
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
import numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
wf=wave.open(sys.argv[1]);A=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs,_=m.transcribe(A,word_timestamps=True,vad_filter=True,beam_size=5,condition_on_previous_text=False,no_repeat_ngram_size=4)
out=[]
for s in segs:
    for w in s.words:out.append({"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2),"p":round(w.probability,2)})
json.dump(out,open(sys.argv[2],"w"))
print(' '.join(f"{x['w']}@{x['s']:.2f}" for x in out))
