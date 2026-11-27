# Speaker embeddings over sliding windows (wespeaker ResNet34-LM, CC BY 4.0) with Kaldi-style fbank in numpy.
# usage: python3 speakers.py a16.wav models/wespeaker_r34.onnx [threads]   -> spk_win.npz (window centres, embeddings, rms)
# Then: python3 label.py  (host = the biggest voice cluster across the file, everyone else = guest)
import numpy as np,wave,onnxruntime as ort,sys,time
SR=16000;WIN=1.5;HOP=0.5
w=wave.open(sys.argv[1]);A=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)   # int16 scale, as Kaldi expects
def mel(f):return 1127.0*np.log(1.0+f/700.0)
def melbanks(nb=80,nfft=512,lo=20.0,hi=8000.0):
    nbin=nfft//2;fw=SR/nfft;ml,mh=mel(lo),mel(hi);d=(mh-ml)/(nb+1);m=mel(fw*np.arange(nbin))
    B=np.zeros((nb,nbin+1),np.float32)
    for b in range(nb):
        l,c,r=ml+b*d,ml+(b+1)*d,ml+(b+2)*d;up=(m-l)/(c-l);dn=(r-m)/(r-c);B[b,:nbin]=np.maximum(0,np.minimum(up,dn))
    return B
MB=melbanks();HAM=(0.54-0.46*np.cos(2*np.pi*np.arange(400)/399)).astype(np.float32)
def fbank(x):
    n=1+(len(x)-400)//160;idx=np.arange(400)[None,:]+160*np.arange(n)[:,None];fr=x[idx].astype(np.float32)
    fr=fr-fr.mean(1,keepdims=True);pre=fr.copy();pre[:,1:]=fr[:,1:]-0.97*fr[:,:-1];pre[:,0]=fr[:,0]-0.97*fr[:,0];fr=pre*HAM
    sp=np.abs(np.fft.rfft(fr,512))**2;f=np.log(np.maximum(sp@MB.T,1.1920929e-07));return f-f.mean(0,keepdims=True)
so=ort.SessionOptions();so.intra_op_num_threads=int(sys.argv[3]) if len(sys.argv)>3 else 2
sess=ort.InferenceSession(sys.argv[2],so,providers=['CPUExecutionProvider'])
cs=np.arange(WIN/2,len(A)/SR-WIN/2,HOP);E=[];R=[];t0=time.time();B=32;batch=[]
for k,c in enumerate(cs):
    x=A[int((c-WIN/2)*SR):int((c+WIN/2)*SR)];R.append(float(np.sqrt((x**2).mean())));batch.append(fbank(x))
    if len(batch)==B or k==len(cs)-1:
        e=sess.run(None,{'feats':np.stack(batch).astype(np.float32)})[0];E.append(e);batch=[]
        if (k//B)%40==0:print(f'{c:7.1f}s / {len(A)/SR:.0f}s  {time.time()-t0:5.0f}s',flush=True)
E=np.concatenate(E);E/=np.linalg.norm(E,axis=1,keepdims=True)
np.savez('spk_win.npz',c=cs,e=E.astype(np.float32),r=np.array(R,np.float32));print('DONE',E.shape,round(time.time()-t0),'s')
