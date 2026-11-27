import numpy as np,cv2
def smooth(x,a,b):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def tone(x,lift=0.012,gamma=1.0,contrast=1.14,pivot=0.44,shoulder=0.80):
    x=np.clip(x,0,1)**gamma
    x=pivot+(x-pivot)*contrast
    hi=x>shoulder
    x=np.where(hi,shoulder+(1-shoulder)*np.tanh((x-shoulder)/(1-shoulder)),x)
    x=np.clip(x,0,1)
    return lift+x*(1-lift)
def grade(img,look='day'):
    """img float32 RGB 0..1. 'day' = terrace (overcast daylight), 'int' = bright interior, 'view' = terrace background shown off"""
    if look=='int':
        x=tone(img*0.93,gamma=1.08,contrast=1.16,pivot=0.46,shoulder=0.76)
    elif look=='view':
        # background plate when the location is the point: stay close to the camera original (it holds the cloud detail),
        # add local contrast, a gentle curve, richer sea and greens
        y=img.astype(np.float32);l0=(0.2126*y[...,0]+0.7152*y[...,1]+0.0722*y[...,2])
        loc=l0-cv2.GaussianBlur(l0,(0,0),30);y=np.clip(y+(loc*0.50)[...,None],0,1)
        x=tone(y,lift=0.0,gamma=1.03,contrast=1.07,pivot=0.50,shoulder=0.92)
    else:
        x=tone(img,gamma=1.04,contrast=1.16,pivot=0.44,shoulder=0.80)
    l=(0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2])[...,None]
    sh=(1-smooth(l,0.0,0.45));hi=smooth(l,0.55,1.0)
    hit=np.array([-0.012,0.0,0.016],dtype=np.float32) if look=='view' else np.array([0.016,0.004,-0.02],dtype=np.float32)
    x=x+sh*np.array([-0.018,0.006,0.022],dtype=np.float32)+hi*hit
    l=(0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2])[...,None]
    # richer view: lift saturation of greens / teals more than the rest
    sat=1.20 if look=='view' else 1.10
    x=l+(x-l)*sat
    lab=cv2.cvtColor(np.clip(x,0,1).astype(np.float32),cv2.COLOR_RGB2Lab)
    hue=np.degrees(np.arctan2(lab[...,2],lab[...,1]));ch=np.hypot(lab[...,1],lab[...,2])
    wv=(smooth(hue,95,135)*(1-smooth(hue,215,250))+smooth(hue,-180,-150)*0+ (hue<-95)*smooth(-hue,95,120))*smooth(ch,3,10)   # greens, teals, blues
    k=1+(0.40 if look=='view' else 0.22)*np.clip(wv,0,1)
    lab[...,1]*=k;lab[...,2]*=k
    return np.clip(cv2.cvtColor(lab,cv2.COLOR_Lab2RGB),0,1)
def decontaminate(img,a,thr=0.92,sigma=5):
    m=(a>thr).astype(np.float32)
    num=cv2.GaussianBlur(img*m[...,None],(0,0),sigma);den=cv2.GaussianBlur(m,(0,0),sigma)[...,None]
    ext=num/np.maximum(den,1e-4)
    w=np.clip((a-0.55)/(thr-0.55),0,1)[...,None]
    ok=(den>0.02)
    return np.where(ok,img*w+ext*(1-w),img)
