# Word-level transcript with faster-whisper (CPU). usage: python3 tr.py audio_16k_mono.wav words.json
# Settings that matter: pass the audio as an array (not a path), VAD on, no initial prompt, no conditioning on previous text
# (otherwise long raws make it loop one sentence). Set HF_HUB_DISABLE_XET=1 if the model download stalls.
import os,json,sys,wave
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
import numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
wf=wave.open(sys.argv[1]);AUD=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs,_=m.transcribe(AUD,word_timestamps=True,vad_filter=True,beam_size=5,condition_on_previous_text=False,no_repeat_ngram_size=4)
out=[]
for s in segs:
    for w in s.words:out.append({"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2)})
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}",flush=True)
json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else "words.json","w"),indent=0)
