# Host or guest label per word from the voice windows, then turns.
# usage: python3 label.py segs.jsonl   (needs spk_win.npz from speakers.py; writes clusters.npy and turns.json)
import sys
from scipy.cluster.hierarchy import linkage,fcluster
from scipy.spatial.distance import pdist
import json,numpy as np
from scipy.ndimage import median_filter
Z=np.load('spk_win.npz');c,E,R=Z['c'],Z['e'],Z['r']
# cluster the louder windows into voices (average linkage, cosine distance 0.62)
idx=np.where(R>np.percentile(R,35))[0];lab=fcluster(linkage(pdist(E[idx],'cosine'),'average'),0.62,'distance');np.save('clusters.npy',np.stack([idx,lab]))
u,n=np.unique(lab,return_counts=True);host=u[np.argmax(n)];hc=E[idx[lab==host]].mean(0);hc/=np.linalg.norm(hc)
# widen the host profile with every cluster that sounds like the host off the mic
hw=np.concatenate([idx[lab==k] for k in u if ((E[idx[lab==k]].mean(0)/np.linalg.norm(E[idx[lab==k]].mean(0)))@hc>0.78 and (lab==k).sum()>=6)])
hc2=E[hw].mean(0);hc2/=np.linalg.norm(hc2);sim=median_filter(E@hc2,size=3,mode='nearest')
segs=[json.loads(l) for l in open(sys.argv[1] if len(sys.argv)>1 else 'segs.jsonl')]
words=[w for s in segs for w in s['w']]
for w in words:
    m=(c>=w['s']-0.2)&(c<=w['e']+0.2);w['h']=float(sim[m].mean()) if m.any() else float(sim[np.argmin(np.abs(c-(w['s']+w['e'])/2))])
TH=0.42
lab_w=['H' if w['h']>TH else 'G' for w in words]
# smoothing: a flip shorter than 3 words between two runs of the same label is absorbed
for i in range(1,len(words)-1):
    j=i
    while j<len(words) and lab_w[j]==lab_w[i]:j+=1
    if j-i<=2 and i>0 and j<len(words) and lab_w[i-1]==lab_w[j] and words[j-1]['e']-words[i]['s']<0.9:
        for k in range(i,j):lab_w[k]=lab_w[i-1]
turns=[]
for w,l in zip(words,lab_w):
    if turns and turns[-1]['who']==l and w['s']-turns[-1]['e']<1.6:turns[-1]['t']+=' '+w['w'];turns[-1]['e']=w['e'];turns[-1]['hs'].append(w['h'])
    else:turns.append({'who':l,'s':w['s'],'e':w['e'],'t':w['w'],'hs':[w['h']]})
for t in turns:t['conf']=round(float(np.mean(t['hs'])),2);del t['hs']
json.dump(turns,open('turns.json','w'))
print('words',len(words),'turns',len(turns),'host words %.0f%%'%(100*sum(1 for l in lab_w if l=='H')/len(lab_w)))
