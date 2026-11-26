import numpy as np,cv2
def smooth(x,a,b):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def tone(x,lift=0.018,gamma=0.96,contrast=1.16,pivot=0.42,shoulder=0.86):
    # filmic-ish: gamma, contrast around pivot, soft shoulder roll-off, slight lift
    x=np.clip(x,0,1)**gamma
    x=pivot+(x-pivot)*contrast
    hi=x>shoulder
    x=np.where(hi,shoulder+(1-shoulder)*np.tanh((x-shoulder)/(1-shoulder)),x)
    x=np.clip(x,0,1)
    return lift+x*(1-lift)
def grade(img,sat=0.94,warm=1.0,variant='A'):
    """img float32 RGB 0..1 -> graded"""
    x=tone(img)
    l=(0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2])[...,None]
    # split tone: teal shadows, warm highlights
    sh=(1-smooth(l,0.0,0.45));hi=smooth(l,0.5,1.0)
    tint_sh=np.array([-0.022,0.004,0.030],dtype=np.float32);tint_hi=np.array([0.030,0.008,-0.030],dtype=np.float32)*warm
    x=x+sh*tint_sh+hi*tint_hi
    l=(0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2])[...,None]
    x=l+(x-l)*sat
    return np.clip(x,0,1)
def decontaminate(img,a,thr=0.92,sigma=5):
    """replace colour of semi-transparent edge pixels with colour extended from solid interior"""
    m=(a>thr).astype(np.float32)
    num=cv2.GaussianBlur(img*m[...,None],(0,0),sigma);den=cv2.GaussianBlur(m,(0,0),sigma)[...,None]
    ext=num/np.maximum(den,1e-4)
    w=np.clip((a-0.55)/(thr-0.55),0,1)[...,None]
    ok=(den>0.02)
    return np.where(ok,img*w+ext*(1-w),img)
