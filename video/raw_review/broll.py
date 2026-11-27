# B-roll finder: stretches with no guest speech where the camera is moving (walking) or the host is quiet.
# usage: python3 broll.py raw.mov   (needs turns.json from label.py) -> kf/ thumbnails, broll.json, broll_sheet.jpg
import json,os,subprocess,sys,numpy as np,cv2
from PIL import Image,ImageDraw
src=sys.argv[1];os.makedirs('kf',exist_ok=True)
if not os.listdir('kf'):
    r=subprocess.run(['ffmpeg','-hide_banner','-skip_frame','nokey','-i',src,'-an','-vf','scale=108:192,showinfo','-vsync','0','-q:v','4','kf/%05d.jpg'],capture_output=True,text=True)
    open('kf_times.txt','w').write('\n'.join(l.split('pts_time:')[1].split()[0] for l in r.stderr.splitlines() if 'pts_time:' in l))
ts=np.array([float(x) for x in open('kf_times.txt')]);N=len(ts);T=json.load(open('turns.json'))
guest=np.zeros(N,bool);host=np.zeros(N,bool)
for t in T:
    m=(ts>=t['s']-0.6)&(ts<=t['e']+0.6)
    if t['who']=='G':guest|=m
    else:host|=m
prev=None;mot=np.zeros(N)
for i in range(N):
    g=cv2.cvtColor(cv2.imread(f'kf/{i+1:05d}.jpg'),cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None:mot[i]=np.abs(g-prev).mean()
    prev=g
out=[];i=0
while i<N:
    if not guest[i]:
        j=i
        while j<N and not guest[j]:j+=1
        a,b=i,min(j,N-1);dur=ts[b]-ts[a];m=float(np.median(mot[a:j]));ht=float(host[a:j].mean())
        if dur>=3 and ht<=0.4 and m>=28:out.append({'s':round(float(ts[a]),1),'e':round(float(ts[b]),1),'dur':round(float(dur),1),'motion':round(m,1),'k':[int(a),int(j)]})
        i=j
    else:i+=1
json.dump(out,open('broll.json','w'),indent=0)
rows=[]
for c in out:
    a,b=c['k'];r=Image.new('RGB',(108*5+150,192),(20,20,20))
    for n,k in enumerate(np.linspace(a+1,b-2,5).astype(int)):r.paste(Image.open(f'kf/{k+1:05d}.jpg').convert('RGB'),(150+n*108,0))
    d=ImageDraw.Draw(r);d.text((6,8),f"{int(c['s']//60)}:{c['s']%60:04.1f}",fill=(255,255,0));d.text((6,24),f"{c['dur']:.1f}s",fill=(200,200,200));rows.append(r)
if rows:
    W=Image.new('RGB',(690*2,192*((len(rows)+1)//2)))
    for n,r in enumerate(rows):W.paste(r,((n%2)*690,(n//2)*192))
    W.save('broll_sheet.jpg',quality=86)
print(len(out),'b-roll stretches, %.0fs'%sum(c['dur'] for c in out))
