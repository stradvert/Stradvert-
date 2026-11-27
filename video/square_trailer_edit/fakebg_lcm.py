# Latent consistency model (SimianLuo/LCM_Dreamshaper_v7, MIT licence) run with onnxruntime only: txt2img and img2img, no PyTorch.
# Download the ONNX folders (text_encoder, unet, vae_decoder, vae_encoder, tokenizer) into ./lcm first, e.g. with huggingface_hub.snapshot_download.
# Sizes must make the latent divisible by 8 (768x448 works). About 16 GB of RAM allows 768x448 per call, not more.
# usage: import fakebg_lcm as lcm; lcm.txt2img(prompt, 768, 448, steps=6, seed=1).save('base.jpg')
import numpy as np,onnxruntime as ort,time
from transformers import CLIPTokenizer
from PIL import Image
D='lcm/'
so=ort.SessionOptions();so.intra_op_num_threads=4;so.enable_cpu_mem_arena=False;so.enable_mem_pattern=False
tok=CLIPTokenizer.from_pretrained(D+'tokenizer')
_s={}
def sess(n):
    if n not in _s:_s[n]=ort.InferenceSession(D+n+'/model.onnx',so,providers=['CPUExecutionProvider'])
    return _s[n]
betas=np.linspace(0.00085**0.5,0.012**0.5,1000,dtype=np.float64)**2;AC=np.cumprod(1-betas)
def embed(p):
    ids=tok(p,padding='max_length',max_length=77,truncation=True,return_tensors='np').input_ids.astype(np.int32)
    return sess('text_encoder').run(None,{'input_ids':ids})[0].astype(np.float32)
def wemb(w,dim=256):
    w=np.array([w*1000.0]);h=dim//2;e=np.exp(np.arange(h)*-(np.log(10000.0)/(h-1)));e=w[:,None]*e[None,:]
    return np.concatenate([np.sin(e),np.cos(e)],1).astype(np.float32)
def timesteps(n,strength=1.0,orig=50):
    o=np.arange(1,int(orig*strength)+1)*(1000//orig)-1;sk=max(1,len(o)//n);return o[::-sk][:n]
def denoise(lat,emb,ts,rng,guidance=8.0,log=True):
    we=wemb(guidance-1)
    for i,t in enumerate(ts):
        t0=time.time()
        eps=sess('unet').run(None,{'sample':lat.astype(np.float32),'timestep':np.array([t],dtype=np.int64),'encoder_hidden_states':emb,'timestep_cond':we})[0].astype(np.float64)
        a=AC[t];x0=(lat-np.sqrt(1-a)*eps)/np.sqrt(a);st=t*10.0;cs=0.25/(st*st+0.25);co=st/np.sqrt(st*st+0.25);den=co*x0+cs*lat
        if i<len(ts)-1:
            ap=AC[ts[i+1]];lat=np.sqrt(ap)*den+np.sqrt(1-ap)*rng.standard_normal(lat.shape)
        else:lat=den
        if log:print(f'  step {i+1}/{len(ts)} t={t} {time.time()-t0:.1f}s',flush=True)
    return lat
def decode(lat):
    x=sess('vae_decoder').run(None,{'latent_sample':(lat/0.18215).astype(np.float32)})[0][0]
    return Image.fromarray((np.clip(x.transpose(1,2,0)/2+0.5,0,1)*255).astype(np.uint8))
def encode(img):
    x=(np.asarray(img.convert('RGB'),dtype=np.float32)/127.5-1).transpose(2,0,1)[None]
    return sess('vae_encoder').run(None,{'sample':x})[0].astype(np.float64)*0.18215
def txt2img(prompt,w=768,h=432,steps=6,seed=0,guidance=8.0):
    rng=np.random.default_rng(seed);lat=rng.standard_normal((1,4,h//8,w//8));return decode(denoise(lat,embed(prompt),timesteps(steps),rng,guidance))
def img2img(img,prompt,strength=0.5,steps=4,seed=0,guidance=8.0):
    rng=np.random.default_rng(seed);ts=timesteps(steps,strength);l0=encode(img);a=AC[ts[0]]
    lat=np.sqrt(a)*l0+np.sqrt(1-a)*rng.standard_normal(l0.shape);return decode(denoise(lat,embed(prompt),ts,rng,guidance))
