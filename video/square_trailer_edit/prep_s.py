# Square edit prep: graded background plates (sharp-ish + soft), skin-matched cutouts, head metrics.
import numpy as np,cv2,json,os,sys
from multiprocessing import Pool
from PIL import Image
from grade import grade,decontaminate
for d in('bg','bgb','fg'):os.makedirs(d,exist_ok=True)
UP=1.3;TARGET_HUE=44.0;TARGET_L=56.0
INT={'p62','stats','close'};NOMATTE={'pave'}
def sm(x,a,b):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def skinfix(rgb,gain):
    lab=cv2.cvtColor(rgb.astype(np.float32),cv2.COLOR_RGB2Lab);L,a,b=lab[...,0],lab[...,1],lab[...,2]
    hue=np.degrees(np.arctan2(b,a));ch=np.hypot(a,b)
    w=sm(hue,-52,-28)*(1-sm(hue,TARGET_HUE-6,TARGET_HUE+2))*sm(ch,3.5,9)*(1-0.45*sm(ch,31,44))*sm(L,14,30)
    pull=np.clip(TARGET_HUE-hue,0,140)*0.8*w
    h2=np.radians(hue+pull);c2=ch*(1-0.25*np.clip(pull/60,0,1))
    lab[...,1]=np.cos(h2)*c2;lab[...,2]=np.sin(h2)*c2
    out=cv2.cvtColor(lab,cv2.COLOR_Lab2RGB)
    if abs(gain-1)>1e-3:
        out=out*gain;hi=out>0.84;out=np.where(hi,0.84+0.16*np.tanh((out-0.84)/0.16),out)
    return np.clip(out,0,1)
def headbox(a2):
    ys,xs=np.where(a2>0.5)
    if len(ys)==0:return None
    top=int(ys.min());band=a2[top:top+220];bx=np.where(band.max(0)>0.5)[0]
    return top,int(np.median(bx)) if len(bx) else int(xs.mean())
def stats(args):
    """median Lab of skin-coloured pixels in the head region (robust to pose)"""
    f,look=args
    img=cv2.cvtColor(cv2.imread(f'fr/{f+1:05d}.jpg'),cv2.COLOR_BGR2RGB).astype(np.float32)/255
    a=cv2.imread(f'al/{f+1:05d}.png',0).astype(np.float32)/255;hb=headbox(a)
    if hb is None:return None
    top,cx=hb;y0,y1,x0,x1=top+60,min(1080,top+520),max(0,cx-260),min(1920,cx+260)
    g=grade(img[y0:y1,x0:x1],look);m=a[y0:y1,x0:x1]>0.9
    lab=cv2.cvtColor(g,cv2.COLOR_RGB2Lab);hue=np.degrees(np.arctan2(lab[...,2],lab[...,1]));ch=np.hypot(lab[...,1],lab[...,2])
    sk=m&(hue>5)&(hue<68)&(ch>11)&(ch<42)&(lab[...,0]>32)&(lab[...,0]<88)
    if sk.sum()<800:return None
    return [float(np.median(lab[...,0][sk])),float(np.median(lab[...,1][sk])),float(np.median(lab[...,2][sk]))]
def one(args):
    f,look,gain,matte=args;name=f'{f+1:05d}'
    img=cv2.cvtColor(cv2.imread(f'fr/{name}.jpg'),cv2.COLOR_BGR2RGB)
    g=grade(img.astype(np.float32)/255,look)
    for d,sig in(('bg',2.0),('bgb',11.0)):
        b=cv2.GaussianBlur(g,(0,0),sig)
        cv2.imwrite(f'{d}/{name}.jpg',cv2.cvtColor((b*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,92 if d=='bg' else 88])
    if not matte:return [f,0,0,2,2,150,960]
    a=cv2.imread(f'al/{name}.png',0).astype(np.float32)/255
    a2=cv2.GaussianBlur(a,(0,0),0.9);a2=np.clip((a2-0.10)/0.86,0,1)
    ys,xs=np.where(a2>0.02)
    if len(ys)==0:return [f,0,0,2,2,150,960]
    x0,x1,y0,y1=max(0,xs.min()-10),min(1920,xs.max()+11),max(0,ys.min()-10),min(1080,ys.max()+11)
    crop=img[y0:y1,x0:x1];ac=a2[y0:y1,x0:x1]
    gc=skinfix(grade(crop.astype(np.float32)/255,look),gain);gc=decontaminate(gc,ac)
    W,H=int(round((x1-x0)*UP)),int(round((y1-y0)*UP))
    up=cv2.resize(gc,(W,H),interpolation=cv2.INTER_LANCZOS4)
    bl=cv2.GaussianBlur(up,(0,0),1.3);up=np.clip(up+(up-bl)*0.45,0,1)
    au=np.clip(cv2.resize(ac,(W,H),interpolation=cv2.INTER_CUBIC),0,1)
    Image.fromarray(np.dstack([(up*255).astype(np.uint8),(au*255).astype(np.uint8)]),'RGBA').save(f'fg/{name}.webp',quality=93,method=3,alpha_quality=100)
    hb=headbox(a2);top,cx=hb if hb else (150,960)
    return [f,int(x0),int(y0),int(x1-x0),int(y1-y0),int(top),int(cx)]
if __name__=='__main__':
    sj=json.load(open('scenes.json'));jobs=[]
    with Pool(4) as p:
        for S in sj['scenes']:
            look='int' if S['key'] in INT else 'day';fr=list(range(S['f0'],S['f1']));matte=S['key'] not in NOMATTE;gain=1.0
            if matte:
                st=[x for x in p.map(stats,[(f,look) for f in fr[::4]]) if x]
                L,a,b=np.median(np.array(st),0) if len(st)>3 else (TARGET_L,14.0,16.0);hue=float(np.degrees(np.arctan2(b,a)));gain=float(np.clip((TARGET_L/L)**0.7,0.95,1.12))
                print(f"{S['key']:8s} {look} skin L {L:.1f} hue {hue:.0f} gain {gain:.2f}",flush=True)
            jobs+=[(f,look,gain,matte) for f in fr]
        res=p.map(one,jobs,chunksize=8)
    json.dump(res,open('fgmeta.json','w'));print('done',len(res))
