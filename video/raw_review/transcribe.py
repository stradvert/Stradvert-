# faster-whisper on a long raw. Segments are written as they are decoded, so you can read along while it runs.
# usage: python3 transcribe.py a16.wav segs   -> segs.jsonl (one segment per line, with words) and segs.words.json
import os,json,sys,wave,time
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
import numpy as np
from faster_whisper import WhisperModel
src,out=sys.argv[1],sys.argv[2]
m=WhisperModel("medium.en",device="cpu",compute_type="int8",cpu_threads=int(os.environ.get('THREADS','4')))
wf=wave.open(src);A=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768;dur=len(A)/16000
segs,info=m.transcribe(A,word_timestamps=True,vad_filter=True,vad_parameters={'min_silence_duration_ms':400},beam_size=5,
                        condition_on_previous_text=False,no_repeat_ngram_size=4,temperature=[0.0,0.2,0.4])
t0=time.time();words=[]
with open(out+'.jsonl','w') as f:
    for s in segs:
        ws=[{'w':w.word.strip(),'s':round(w.start,2),'e':round(w.end,2),'p':round(w.probability,2)} for w in s.words]
        words+=ws
        f.write(json.dumps({'s':round(s.start,2),'e':round(s.end,2),'t':s.text.strip(),'lp':round(s.avg_logprob,2),'ns':round(s.no_speech_prob,2),'w':ws})+'\n');f.flush()
        print(f'{s.end/dur*100:5.1f}%  {s.end:7.1f}s  elapsed {time.time()-t0:6.0f}s',flush=True)
json.dump(words,open(out+'.words.json','w'))
print('DONE',len(words),'words',round(time.time()-t0),'s',flush=True)
