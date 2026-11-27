# Phone screen recording -> card frames, with the start of the route hidden.
# The map pans and zooms through the clip, so the blue "you are here" dot is found in every frame and a soft blur
# follows it (wide enough to take in the name of the place next to it). Frames before T_MAP are the search list.
import subprocess,os,shutil,sys,numpy as np,cv2
SRC=os.environ.get('SRC','raw.mp4');T0,T1=16.95,22.50;T_MAP=18.80          # T0 is after anything private at the top of the recording (saved addresses, recent searches)
# what the card plays: the typing, then straight to the route once the map has zoomed in (the wide map before that would need most of it blurred)
PLAY=[(16.95,18.78),(20.82,22.50)];SPEED=float(os.environ.get('SPEED','1.3'));HOLD=float(os.environ.get('HOLD','0.5'));CROP=(97,118,886,1800);OUTN=int(sys.argv[1]) if len(sys.argv)>1 else 90;OUTW=620
shutil.rmtree('tmp/mp',ignore_errors=True);os.makedirs('tmp/mp')
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(T0),'-t',str(T1-T0),'-i',SRC,'-an','-vf',f'fps=30,crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]}','-q:v','2','tmp/mp/%05d.jpg'],check=True)
fs=sorted(os.listdir('tmp/mp'));N=len(fs)
def blobs(mask,amin,amax):
    n,lab,st,cen=cv2.connectedComponentsWithStats(mask.astype(np.uint8),8);out=[]
    for i in range(1,n):
        a=st[i,cv2.CC_STAT_AREA];w=st[i,cv2.CC_STAT_WIDTH];h=st[i,cv2.CC_STAT_HEIGHT]
        if amin<=a<=amax and 0.6<w/max(h,1)<1.7:out.append((a,cen[i][0],cen[i][1],w,h))
    return sorted(out,reverse=True)
dot=[None]*N;pin=[None]*N;sheet=[1300]*N
for i,f in enumerate(fs):
    t=T0+i/30
    if t<T_MAP:continue
    im=cv2.imread('tmp/mp/'+f);hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV);H,Sat,V=hsv[...,0].astype(int)*2,hsv[...,1],hsv[...,2]
    # where the white bottom sheet starts (the map sits above it)
    row=(im.min(2)>235).mean(1);ys=np.where(row[300:]>0.92)[0];top=300+ys[0] if len(ys) else 1300;sheet[i]=top
    m=(H>=204)&(H<=230)&(Sat>150)&(V>170);m[:150]=False;m[top-8:]=False
    b=blobs(m,170,1100)
    if b:dot[i]=(b[0][1],b[0][2])
    r=((H<=8)|(H>=352))&(Sat>170)&(V>170);r[:150]=False;r[top-8:]=False
    b=blobs(r,150,6000)
    if b:pin[i]=(b[0][1],b[0][2])
def fill(seq):
    idx=[i for i,v in enumerate(seq) if v is not None]
    if not idx:return seq
    out=list(seq)
    for i in range(N):
        if out[i] is None:
            if i<idx[0]:continue
            p=max(j for j in idx if j<=i) if any(j<=i for j in idx) else idx[0];q=min([j for j in idx if j>=i],default=p)
            if p==q:out[i]=seq[p]
            else:
                a=(i-p)/(q-p);out[i]=(seq[p][0]*(1-a)+seq[q][0]*a,seq[p][1]*(1-a)+seq[q][1]*a)
    return out
# reject jumps (a route dot mistaken for the location dot), then fill and smooth
for i in range(1,N):
    if dot[i] is not None and dot[i-1] is not None and np.hypot(dot[i][0]-dot[i-1][0],dot[i][1]-dot[i-1][1])>90:
        nxt=next((dot[j] for j in range(i+1,min(N,i+6)) if dot[j] is not None),None)
        if nxt is not None and np.hypot(nxt[0]-dot[i-1][0],nxt[1]-dot[i-1][1])<90:dot[i]=None
dot=fill(dot);pin=fill(pin)
first=next(i for i,v in enumerate(dot) if v is not None)
os.makedirs('m',exist_ok=True);[os.remove('m/'+x) for x in os.listdir('m')]
info=[];Dlast=220.0
proc=[]
for i,f in enumerate(fs):
    im=cv2.imread('tmp/mp/'+f);t=T0+i/30
    if t>=T_MAP:
        d=dot[i] if dot[i] is not None else dot[first]
        if pin[i] is not None:Dlast=float(np.hypot(pin[i][0]-d[0],pin[i][1]-d[1]))
        # the place name next to the dot is a fixed size on screen and its marker moves away slowly as the map zooms in,
        # so the patch only needs to grow a little with the zoom (D = distance from the dot to the destination pin)
        D=Dlast;cx,cy=d[0]+0.03*D-10,d[1]-0.105*D;r=0.11*D+125
        top=sheet[i];yy,xx=np.mgrid[0:im.shape[0],0:im.shape[1]];dist=np.hypot((xx-cx)/1.15,yy-cy)
        m=np.clip((1.35*r-dist)/(0.35*r),0,1);m=m*m*(3-2*m);m[top-4:]=0;m[:150]=0
        bl=cv2.GaussianBlur(im,(0,0),26);bl=cv2.GaussianBlur(bl,(0,0),14);im=(im*(1-m[...,None])+bl*m[...,None]).astype(np.uint8)
        info.append((i,round(t,2),int(d[0]),int(d[1]),int(D),int(r),dot[i] is not None))
    proc.append(im)
seq=[]
for (a,b) in PLAY:
    n=int(round((b-a)/SPEED*30));part=[min(N-1,int(round((a+(b-a)*k/max(1,n-1)-T0)*30))) for k in range(n)]
    seq.append(part)
frames=[proc[i] for i in seq[0]]
for pi in range(1,len(seq)):                      # 3 frame cross-fade at each join
    nxt=[proc[i] for i in seq[pi]]
    for q in range(3):
        a=(q+1)/4.0;frames[-3+q]=cv2.addWeighted(frames[-3+q],1-a,nxt[0],a,0)
    frames+=nxt
frames+=[frames[-1]]*int(HOLD*30);OUTN=len(frames)
for k,im in enumerate(frames):
    h=int(round(im.shape[0]*OUTW/im.shape[1]));cv2.imwrite(f'm/{k+1:05d}.jpg',cv2.resize(im,(OUTW,h),interpolation=cv2.INTER_AREA),[cv2.IMWRITE_JPEG_QUALITY,93])
print('source frames',N,'card frames',OUTN,'= %.2fs;'%(OUTN/30),'route starts at card frame',len(seq[0]),'(%.2fs), walk tab at about %.2fs'%(len(seq[0])/30,(len(seq[0])+(21.50-PLAY[1][0])/SPEED*30)/30));print('dot found in',sum(1 for x in info if x[6]),'of',len(info),'map frames')
# check sheet: every 6th map frame with the blur applied
sel=[i for i in range(N) if T0+i/30>=PLAY[1][0]-0.001][::4];tiles=[cv2.resize(proc[i][150:1300],(443,575)) for i in sel]
for j,i in enumerate(sel):cv2.putText(tiles[j],f'{T0+i/30:.2f}',(6,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
rows=[np.hstack(tiles[k:k+7]+[np.zeros_like(tiles[0])]*(7-len(tiles[k:k+7]))) for k in range(0,len(tiles),7)]
cv2.imwrite('tmp/mapblur_check.jpg',np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])       # look at this sheet before using the card
