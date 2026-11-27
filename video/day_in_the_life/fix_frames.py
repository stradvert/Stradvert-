# Per-segment picture fixes on the extracted frames: punch in on the laptop for the work shots, and blur the meeting title
# (it shows the other person's name). Reads frames_raw/, writes frames/.
import json,cv2,numpy as np,sys
D=json.load(open('segs.json'));T={x['key']:x for x in D['segs']}
PUNCH={'w2':(310,540,760),'w3':(310,540,760),'w5':(250,520,780)}     # x0, y0, width of a 9:16 window in the source frame
BLUR={'w2':[(575,1240,785,1335)]}                                   # boxes in source pixels
LIFT={'r3':1.32}                                                    # gamma lift for a backlit shot
for k,g in LIFT.items():
    lut=np.array([255*((i/255)**(1/g)) for i in range(256)],np.float32)
    for f in range(T[k]['f0'],T[k]['f1']):
        im=cv2.imread(f'frames_raw/{f+1:05d}.jpg');out=lut[im];l=out.mean(2,keepdims=True);out=np.clip(l+(out-l)*1.08,0,255)
        cv2.imwrite(f'frames/{f+1:05d}.jpg',out.astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
    print(k,'lifted',g)
for k,(x0,y0,w) in PUNCH.items():
    h=int(round(w*16/9))
    for f in range(T[k]['f0'],T[k]['f1']):
        im=cv2.imread(f'frames_raw/{f+1:05d}.jpg')
        for (a,b,c,d) in BLUR.get(k,[]):
            roi=im[b:d,a:c];sm=cv2.GaussianBlur(roi,(0,0),9);m=np.zeros(roi.shape[:2],np.float32);m[8:-8,8:-8]=1;m=cv2.GaussianBlur(m,(0,0),5)[...,None]
            im[b:d,a:c]=(roi*(1-m)+sm*m).astype(np.uint8)
        cr=im[y0:y0+h,x0:x0+w];up=cv2.resize(cr,(1080,1920),interpolation=cv2.INTER_LANCZOS4)
        bl=cv2.GaussianBlur(up,(0,0),1.6);up=cv2.addWeighted(up,1.35,bl,-0.35,0)
        cv2.imwrite(f'frames/{f+1:05d}.jpg',up,[cv2.IMWRITE_JPEG_QUALITY,95])
    print(k,'frames',T[k]['f0'],T[k]['f1'],'window',x0,y0,w,h)
