import json,sys,wave
import numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
wf=wave.open(sys.argv[1]); AUD=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs,_=m.transcribe(AUD,word_timestamps=True,vad_filter=False,beam_size=5,initial_prompt="Stradvert, street interview ads, Claude, street polling.")
out=[]
for s in segs:
    for w in s.words: out.append({"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2)})
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
json.dump(out,open("words.json","w"),indent=0)
