# Forced alignment (wav2vec2 CTC, ONNX) of chosen stretches of a raw, to get word edges to about 20 ms.
# Usage: python3 align.py a16.wav words.json spans.json model_dir out.json [merge.json]
#   words.json: transcribe.py words [{w,s,e,...}]; spans.json: [["key", t0, t1], ...]; model_dir holds model.onnx and vocab.json.
# The transcript only supplies the word order. Start times are good; an end time is the last letter, so leave a little after it.
import json,re,sys,wave,numpy as np,onnxruntime as ort
A16,WJ,SPANS,MD,OUT=sys.argv[1:6]
SR=16000
w=wave.open(A16);A=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
W=json.load(open(WJ))
V=json.load(open(MD+'/vocab.json'))
so=ort.SessionOptions();so.intra_op_num_threads=4
S=ort.InferenceSession(MD+'/model.onnx',so,providers=['CPUExecutionProvider'])
iname=S.get_inputs()[0].name
NUM={'95':'NINETY FIVE','95.':'NINETY FIVE','Errrr,':'ER'}
def norm(t):
    t=NUM.get(t,t);t=t.upper().replace('-',' ')
    t=re.sub(r"[^A-Z' ]","",t);return [x for x in t.split() if x.strip("'")]
def region(t0,t1):
    # widen to gaps of 0.25 s or more so no word is cut in half
    ws=sorted(W,key=lambda x:x['s'])
    a,b=t0,t1
    for _ in range(40):
        inside=[x for x in ws if x['e']>a and x['s']<b]
        na=min([a]+[x['s']-0.15 for x in inside]);nb=max([b]+[x['e']+0.15 for x in inside])
        if na==a and nb==b:break
        a,b=na,nb
    return a,b,[x for x in ws if x['e']>a and x['s']<b]
MERGE=json.load(open(sys.argv[6])) if len(sys.argv)>6 else []   # optional [["first","second","Joined"], ...]: a name the transcript splits in two
def merge(ws):
    out=[];i=0
    while i<len(ws):
        a=ws[i]['w'].lower().strip('?,.!');b=ws[i+1]['w'].lower().strip('?,.!') if i+1<len(ws) else ''
        hit=[m for m in MERGE if a==m[0] and b==m[1]]
        if hit:out.append({'w':hit[0][2]+ws[i+1]['w'][len(b):],'s':ws[i]['s'],'e':ws[i+1]['e']});i+=2
        else:out.append(ws[i]);i+=1
    return out
def viterbi(lp,tok):
    T=lp.shape[0];L=len(tok);S_=[0]
    for c in tok:S_+= [c,0]
    S_=np.array(S_);N=len(S_);NEG=-1e9
    dp=np.full((T,N),NEG);bp=np.zeros((T,N),dtype=np.int8)
    dp[0,0]=lp[0,S_[0]];dp[0,1]=lp[0,S_[1]]
    for t in range(1,T):
        p0=dp[t-1];p1=np.concatenate([[NEG],p0[:-1]]);p2=np.concatenate([[NEG,NEG],p0[:-2]])
        ok2=np.zeros(N,bool);ok2[2:]=(S_[2:]!=0)&(S_[2:]!=S_[:-2])
        p2=np.where(ok2,p2,NEG)
        st=np.stack([p0,p1,p2]);k=st.argmax(0);dp[t]=st.max(0)+lp[t,S_];bp[t]=k
    s=N-1 if dp[-1,N-1]>=dp[-1,N-2] else N-2
    path=[0]*T
    for t in range(T-1,-1,-1):
        path[t]=s;s-=int(bp[t,s])
    return S_,path
def align(t0,t1):
    a,b,ws=region(t0,t1)
    x=A[int(a*SR):int(b*SR)].copy();x=(x-x.mean())/np.sqrt(x.var()+1e-7)
    lg=S.run(None,{iname:x[None,:]})[0][0]
    lp=lg-np.log(np.exp(lg-lg.max(1,keepdims=True)).sum(1,keepdims=True))-lg.max(1,keepdims=True)
    ws=merge(ws)
    words=[];tok=[];owner=[]
    for i,x_ in enumerate(ws):
        for p in norm(x_['w']):
            if tok:tok.append(V['|']);owner.append(-1)
            for ch in p:tok.append(V[ch]);owner.append(len(words))
            words.append({'w':x_['w'] if len(norm(x_['w']))==1 else p.lower(),'ws':x_['s'],'we':x_['e']})
    S_,path=viterbi(lp,tok)
    T=lp.shape[0];fd=(b-a)/T
    sp={}
    for t,s in enumerate(path):
        if s%2==1:
            o=owner[(s-1)//2]
            if o>=0:sp.setdefault(o,[t,t]);sp[o][1]=t
    for i,wd in enumerate(words):
        f=sp.get(i,[0,0]);wd['s']=round(a+f[0]*fd,3);wd['e']=round(a+(f[1]+1)*fd,3)
        fr=[t for t,s in enumerate(path) if s%2==1 and owner[(s-1)//2]==i];wd['conf']=round(float(np.mean([np.exp(lp[t,S_[path[t]]]) for t in fr])) if fr else 0,2)
    return {'a':a,'b':b,'words':words}
SEG=json.load(open(SPANS))
out={}
for k,t0,t1 in SEG:
    r=align(t0,t1);out[k]=r
    print(k,f"{r['a']:.2f}-{r['b']:.2f}",' '.join(f"{x['w']}@{x['s']:.2f}-{x['e']:.2f}({x['conf']})" for x in r['words']),flush=True)
json.dump(out,open(OUT,'w'),indent=0)
