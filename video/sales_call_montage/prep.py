# builds: bg/%05d.jpg (graded, pre-blurred 1920x1080), fg/%05d.webp (graded, skin-corrected, decontaminated cutout at 1.5x, cropped)
import numpy as np,cv2,json,os,sys
from multiprocessing import Pool
from PIL import Image
from grade import grade,decontaminate
os.makedirs('bg',exist_ok=True);os.makedirs('fg',exist_ok=True)
UP=1.5;TARGET_HUE=44.0;TARGET_L=51.0
def sm(x,a,b):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def skinfix(rgb,dh,gain):
    """pull pink / magenta (screen-lit) skin toward a natural warm hue pixel by pixel, then match exposure. rgb float 0..1"""
    lab=cv2.cvtColor(rgb.astype(np.float32),cv2.COLOR_RGB2Lab);L,a,b=lab[...,0],lab[...,1],lab[...,2]
    hue=np.degrees(np.arctan2(b,a));ch=np.hypot(a,b)
    # weight: anything from purple-magenta (-80deg) up to the target hue, with some chroma, not too dark; ease off on very saturated reds (lips)
    w=sm(hue,-52,-28)*(1-sm(hue,TARGET_HUE-6,TARGET_HUE+2))*sm(ch,3.5,9)*(1-0.45*sm(ch,31,44))*sm(L,14,30)
    pull=np.clip(TARGET_HUE-hue,0,140)*0.82*w
    h2=np.radians(hue+pull)
    # magenta highlights carry too much chroma for skin once rotated: tame it, more so the further they were pulled
    c2=ch*(1-0.28*np.clip(pull/60,0,1))
    lab[...,1]=np.cos(h2)*c2;lab[...,2]=np.sin(h2)*c2
    out=cv2.cvtColor(lab,cv2.COLOR_Lab2RGB)
    if abs(gain-1)>1e-3:
        out=out*gain;hi=out>0.84;out=np.where(hi,0.84+0.16*np.tanh((out-0.84)/0.16),out)
    return np.clip(out,0,1)
def stats(args):
    f,top,cx=args
    img=cv2.cvtColor(cv2.imread(f'fr/{f+1:05d}.jpg'),cv2.COLOR_BGR2RGB).astype(np.float32)/255
    p=grade(img[top+105:top+195,max(0,cx-65):cx+65]).reshape(-1,3)
    lab=cv2.cvtColor(p[None],cv2.COLOR_RGB2Lab)[0];L,a,b=np.median(lab,0);return [f,float(L),float(a),float(b)]
def one(args):
    f,dh,gain=args;name=f'{f+1:05d}'
    img=cv2.cvtColor(cv2.imread(f'fr/{name}.jpg'),cv2.COLOR_BGR2RGB)
    a=cv2.imread(f'al/{name}.png',0).astype(np.float32)/255
    a2=cv2.GaussianBlur(a,(0,0),0.9);a2=np.clip((a2-0.10)/0.86,0,1)   # slight choke + feather
    g=grade(img.astype(np.float32)/255)
    bg=cv2.GaussianBlur(g,(0,0),9)
    cv2.imwrite(f'bg/{name}.jpg',cv2.cvtColor((bg*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,90])
    ys,xs=np.where(a2>0.02)
    if len(ys)==0:return [f,0,0,2,2,0,0]
    x0,x1,y0,y1=max(0,xs.min()-10),min(1920,xs.max()+11),max(0,ys.min()-10),min(1080,ys.max()+11)
    crop=img[y0:y1,x0:x1];ac=a2[y0:y1,x0:x1]
    den=cv2.fastNlMeansDenoisingColored(cv2.cvtColor(crop,cv2.COLOR_RGB2BGR),None,2,3,5,15)
    den=cv2.cvtColor(den,cv2.COLOR_BGR2RGB).astype(np.float32)/255
    gc=skinfix(grade(den),dh,gain);gc=decontaminate(gc,ac)
    W,H=int(round((x1-x0)*UP)),int(round((y1-y0)*UP))
    up=cv2.resize(gc,(W,H),interpolation=cv2.INTER_LANCZOS4)
    bl=cv2.GaussianBlur(up,(0,0),1.5);up=np.clip(up+(up-bl)*0.6,0,1)
    au=np.clip(cv2.resize(ac,(W,H),interpolation=cv2.INTER_CUBIC),0,1)
    rgba=np.dstack([(up*255).astype(np.uint8),(au*255).astype(np.uint8)])
    Image.fromarray(rgba,'RGBA').save(f'fg/{name}.webp',quality=93,method=3,alpha_quality=100)
    top=int(ys.min());band=a2[top:top+150];bx=np.where(band.max(0)>0.5)[0]
    return [f,int(x0),int(y0),int(x1-x0),int(y1-y0),top,int(bx.mean()) if len(bx) else int(xs.mean())]
if __name__=='__main__':
    sj=json.load(open('scenes.json'));meta={m[0]:m for m in json.load(open('fgmeta.json'))}
    jobs=[]
    with Pool(4) as p:
        for S in sj['scenes']:
            fr=list(range(S['f0'],S['f1']));st=p.map(stats,[(f,meta[f][5],meta[f][6]) for f in fr[::3]])
            L,a,b=np.median(np.array(st)[:,1:],0);hue=float(np.degrees(np.arctan2(b,a)))
            dh=float(np.clip(TARGET_HUE-hue,0,28));gain=float(np.clip((TARGET_L/L)**0.75,0.94,1.2))
            print(f"{S['key']:8s} skin L {L:.1f} hue {hue:.0f} -> rotate {dh:.0f} deg, gain {gain:.2f}",flush=True)
            jobs+=[(f,dh,gain) for f in fr]
        res=p.map(one,jobs,chunksize=8)
    json.dump(res,open('fgmeta.json','w'));print('done',len(res))
