import os,sys,json,re,wave,numpy as np
os.environ['HF_HUB_DISABLE_XET']='1'
from faster_whisper import WhisperModel
w=wave.open(sys.argv[1]);a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
m=WhisperModel('medium.en',device='cpu',compute_type='int8',cpu_threads=2)
segs,_=m.transcribe(a,language='en',word_timestamps=True,vad_filter=True,condition_on_previous_text=False,no_repeat_ngram_size=4)
hyp=[];words=[]
for s in segs:
    for x in s.words:hyp.append(x.word);words.append((x.word.strip(),round(x.start,2)))
norm=lambda s:re.sub(r"[^a-z0-9 ]","",s.lower().replace('%',' percent ').replace('€',' ')).split()
ref=json.load(open('words_cut.json'));R=norm(' '.join(x['w'] for x in ref));H=norm(' '.join(hyp))
# word error rate (Levenshtein)
d=np.zeros((len(R)+1,len(H)+1),int);d[:,0]=np.arange(len(R)+1);d[0,:]=np.arange(len(H)+1)
for i in range(1,len(R)+1):
    for j in range(1,len(H)+1):d[i,j]=min(d[i-1,j]+1,d[i,j-1]+1,d[i-1,j-1]+(R[i-1]!=H[j-1]))
print('ref words',len(R),'hyp words',len(H),'errors',int(d[-1,-1]),'WER %.1f%%'%(100*d[-1,-1]/len(R)))
print('HYP:',' '.join(hyp))
json.dump(words,open(sys.argv[2],'w'))
