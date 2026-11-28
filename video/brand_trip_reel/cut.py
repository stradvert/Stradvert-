# Multi-source cutter for 60 fps portrait raws: picture to 30 fps frames, voice stem with clean fades.
# usage: python3 cut.py edl.json rawdir audiodir   (AUDIO_ONLY=1 rebuilds just the voice)
# edl: [{k, src, a, b, ain?, aout?, fin?, fout?, dn?}]  a, b in source seconds; b-a must be a whole number of 30 fps frames.
import json,os,sys,subprocess,shutil,numpy as np,soundfile as sf
FPS=30;SR=48000
E=json.load(open(sys.argv[1]));RAW=sys.argv[2];AUD=sys.argv[3]
AO=os.environ.get('AUDIO_ONLY')
if not AO:shutil.rmtree('frames',ignore_errors=True)
os.makedirs('frames',exist_ok=True)
cache={}
def aud(src):
    if src not in cache:
        o,_=sf.read(f'{AUD}/{src}.48.wav');d,_=sf.read(f'{AUD}/{src}.dn48.wav');d=d[480:];n=min(len(o),len(d));cache[src]=(o[:n],d[:n])   # arnndn runs 10 ms late
    return cache[src]
fi=1;voice=[];segs=[];t0=0.0
for e in E:
    a,b=e['a'],e['b'];nf=int(round((b-a)*FPS));assert abs((b-a)*FPS-nf)<0.02,(e['k'],'not whole frames',(b-a)*FPS)
    if not AO:
        tmp=f"tmp_{e['k']}";shutil.rmtree(tmp,ignore_errors=True);os.makedirs(tmp)
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f"{a:.4f}",'-i',f"{RAW}/{e['src']}.MOV",'-vf','fps=30,unsharp=5:5:0.3,format=yuvj420p','-frames:v',str(nf),'-q:v','2',f'{tmp}/%05d.jpg'],check=True)
        got=sorted(os.listdir(tmp));assert len(got)>=nf-1,(e['k'],len(got),nf)
        while len(got)<nf:shutil.copy(f'{tmp}/{got[-1]}',f'{tmp}/zz{len(got):04d}.jpg');got=sorted(os.listdir(tmp))
        for g in got[:nf]:os.replace(f'{tmp}/{g}',f'frames/{fi:05d}.jpg');fi+=1
        shutil.rmtree(tmp)
    else:fi+=nf
    o,d=aud(e['src']);mix=e.get('dn',0.5)
    i0=int(round(a*SR));te=e.get('aend',max(b,e.get('aout',b)));i1=i0+int(round((te-a)*SR))
    x=(1-mix)*o[i0:i1]+mix*d[i0:i1]
    L=int(round(nf/FPS*SR));x=np.pad(x,(0,max(0,L-len(x))))
    g=np.ones(len(x));j0=max(0,int(round((e.get('ain',a)-a)*SR)));g[:j0]=0
    fin=int(e.get('fin',0.008)*SR);fout=int(e.get('fout',0.012)*SR);end=int(round((te-a)*SR))
    g[j0:j0+fin]=np.minimum(g[j0:j0+fin],np.linspace(0,1,fin)**1.5);g[end:]=0;g[end-fout:end]=np.minimum(g[end-fout:end],np.linspace(1,0,fout)**1.5)
    x=x*g
    tail=x[L:];x=x[:L]
    if voice and len(tail)==0:pass
    voice.append(x)
    if len(tail):                      # aout spill: overlap the head of the next piece
        voice.append(('spill',tail))
    segs.append({**e,'t0':t0,'t1':t0+nf/FPS,'f0':fi-nf});t0+=nf/FPS
out=np.zeros(int(round(t0*SR))+SR);p=0
for v in voice:
    if isinstance(v,tuple):out[p:p+len(v[1])]+=v[1];continue
    out[p:p+len(v)]+=v;p+=len(v)
out=out[:int(round(t0*SR))]
sf.write('voice_raw.wav',out.astype(np.float32),SR,subtype='FLOAT');json.dump(segs,open('segs_out.json','w'),indent=1)
print('frames',fi-1,'dur',round(t0,3))
