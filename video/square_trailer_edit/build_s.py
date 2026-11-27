# Scene data for the composition: caption groups ([word] = emphasised), word times matched to the cut transcript, head track.
# Worked example. The proof figure is a placeholder here (€000,000): put the number that is spoken in the video.
import json,re,wave,numpy as np
from scipy.ndimage import gaussian_filter1d
sj=json.load(open('scenes.json'));cw=json.load(open('words_cut.json'));meta=json.load(open('fgmeta.json'))
# caption groups per scene; [word] = emphasised
CAP={'hook':["I make ads for a living","and I would [never] do an ad","with a [view] [like] [this.]"],
'reason':["The reason is very simple, because","the more [polished] it looks,","the more [prepared] it looks,","the more [fake] it looks."],
'proof':["My best ads that have had","[€000,000] spend on it","in a couple months,","they [look] [real.]"],
'pave':["They've been filmed","[on] [a] [pavement.]","It looked [real.]","It was [organic.]","It was [off] [the] [cuff.]"],
'ugc':["By now people know that","UGC is people being","[paid] [to] [say] [things.]","People saying it","[on] [the] [street]","is the [absolute] [fix.]"],
'aiview':["I could [fake] [this] [view]","right here,","quite easily, [with] [AI,]","and you'd [never] [know.]","And I don't think you'd care either."],
'rain':["Look at the rain, it's starting to rain,","so I'm gonna have to take this inside.","Let's go."],
'p62':["However,","if you [fake] [the] [person]","that's standing in it,","[62%] of Americans","say that is [unacceptable,]","even if you admit it's AI."],
'stats':["Marketers have it [backwards.]","[82%] of ad execs think","that young consumers like AI ads.","The truth is [45%] of them do."],
'close':["Of course I've used AI before.","But I will [never] use","a [fake] [human] in an ad."]}
norm=lambda s:re.sub(r"[^a-z0-9']","",s.lower())
AL={'€000000':'000','62':'62','82':'82','45':'45','marketers':'markets',"i'm":"we're",'look':'look'}
def key(s):
    k=norm(s);return AL.get(k,k)
INT={'p62','stats','close'}
mm={m[0]:m for m in meta};out=[];caps=[];trk={}
for S in sj['scenes']:
    k=S['key'];t0=S['f0']/30;t1=S['f1']/30
    cand=[(norm(w['w']),w['s'],w['e']) for w in cw if t0-0.22<=w['s']<t1+0.02]
    words=[];groups=[]
    for g in CAP[k]:
        a=len(words)
        for tok in g.split():
            em=tok.startswith('[');txt=tok.strip('[]');words.append([txt,None,1 if em else 0])
        groups.append([a,len(words)])
    j=0;n=len(words)
    for i,w in enumerate(words):
        kk=key(w[0].replace('€','').replace(',','').replace('%','')) if not w[0].startswith('€') else '000'
        for q in range(j,min(j+5,len(cand))):
            if cand[q][0]==kk or (kk and cand[q][0].startswith(kk) and len(kk)>3):w[1]=max(t0,cand[q][1]);j=q+1;break
    lastend=max([c[2] for c in cand]) if cand else t1
    miss=[w[0] for w in words if w[1] is None]
    for i in range(n):
        if words[i][1] is None:
            p=next((x for x in range(i-1,-1,-1) if words[x][1] is not None),None);q=next((x for x in range(i+1,n) if words[x][1] is not None),None)
            a_=words[p][1] if p is not None else t0+0.04;b_=words[q][1] if q is not None else min(t1-0.15,lastend)
            pi=p if p is not None else -1;qi=q if q is not None else n
            words[i][1]=a_+(b_-a_)*(i-pi)/(qi-pi)
    for i in range(1,n):words[i][1]=max(words[i][1],words[i-1][1]+0.02)
    for w in words:w[1]=round(float(w[1]),3)
    for gi,(a,b) in enumerate(groups):
        s=words[a][1];e=words[groups[gi+1][0]][1]-0.02 if gi+1<len(groups) else t1
        caps.append({'sc':k,'a':a,'b':b,'s':round(s,3),'e':round(e,3)})
    fr=list(range(S['f0'],S['f1']));cx=np.array([mm[f][6] for f in fr],float);tp=np.array([mm[f][5] for f in fr],float)
    # smooth the head track within each shot (jump cuts must not smear)
    for a,b in S['shots']:
        ia,ib=a-S['f0'],b-S['f0']
        for arr in(cx,tp):
            seg=arr[ia:ib];med=np.median(seg);mad=np.median(np.abs(seg-med))+3;seg=np.clip(seg,med-6*mad,med+6*mad);arr[ia:ib]=gaussian_filter1d(seg,6,mode='nearest')
    for i,f in enumerate(fr):trk[str(f)]=[round(float(cx[i]),1),round(float(tp[i]),1)]
    print(f"{k:8s} unmatched {miss}  head top {np.median(tp):.0f} cx {np.median(cx):.0f}")
    out.append({'key':k,'s':round(t0,4),'e':round(t1,4),'f0':S['f0'],'f1':S['f1'],'shots':S['shots'],'look':'int' if k in INT else 'day','top':float(np.median(tp)),'cx':float(np.median(cx)),'w':words})
wf=wave.open('a16c.wav');a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
nf=sj['nf'];env=[float(np.sqrt((a[int(f/30*16000):int((f+1)/30*16000)]**2).mean()+1e-12)) for f in range(nf)]
m=np.percentile(env,95);env=[round(min(1,e/m),3) for e in env]
END=84
json.dump({'sc':out,'caps':caps,'nf':nf,'vd':nf/30,'total':nf+END,'fg':{str(m[0]):m[1:5] for m in meta},'env':env,'trk':trk},open('data.json','w'))
print('nf',nf,'total',nf+END,(nf+END)/30)
