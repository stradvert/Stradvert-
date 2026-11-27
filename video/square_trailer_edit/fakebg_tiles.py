# Upscale a 768x448 base image to 2240x1280 by refining overlapping 768x448 tiles (img2img at low strength), then feather-blend.
# Only the tiles that will be on screen are refined. usage: python3 fakebg_tiles.py   (reads c_dump_1.jpg, writes dump_final.png)
import fakebg_lcm as lcm,time,numpy as np,sys,os
from PIL import Image,ImageOps
P="wide angle photo of a vast landfill rubbish dump, mountains of garbage bags and trash, muddy ground with puddles, grey overcast sky, bleak, empty, no people, realistic dslr photograph, sharp focus, detailed"
t0=time.time();TW,TH=768,448;W,H=2240,1280
big=ImageOps.mirror(Image.open('c_dump_1.jpg')).resize((W,H),Image.LANCZOS)
xs=(0,491,982);ys=(0,416,832);os.makedirs('tiles',exist_ok=True);k=0   # the column at x 1472 is never on screen
for y in ys:
    for x in xs:
        p=f'tiles/{y}_{x}.png'
        if not os.path.exists(p):
            lcm.img2img(big.crop((x,y,x+TW,y+TH)),P,strength=0.4,steps=3,seed=20+k).save(p);print('tile',y,x,round(time.time()-t0),'s',flush=True)
        k+=1
acc=np.asarray(big,dtype=np.float64)*1e-3;wsum=np.full((H,W,1),1e-3)
for y in ys:
    for x in xs:
        t=np.asarray(Image.open(f'tiles/{y}_{x}.png'),dtype=np.float64)
        wx=np.minimum(np.arange(TW)+1,TW-np.arange(TW));wy=np.minimum(np.arange(TH)+1,TH-np.arange(TH))
        w=(np.clip(wx/240,0,1)[None,:]*np.clip(wy/30,0,1)[:,None])[...,None]
        acc[y:y+TH,x:x+TW]+=t*w;wsum[y:y+TH,x:x+TW]+=w
Image.fromarray(np.clip(acc/wsum,0,255).astype(np.uint8)).save('dump_final.png');print('done',round(time.time()-t0),'s',flush=True)
