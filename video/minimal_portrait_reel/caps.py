# Group word timings into short caption groups for the minimal portrait edit.
# usage: python3 caps.py words.json data.json     (adds "caps" and "lastEnd" to data.json, keeps everything else)
# words.json is the word list of the CUT (not the raw): [{"w":"word","s":start,"e":end}, ...]
import json,sys
W=json.load(open(sys.argv[1]));p=sys.argv[2]
try:D=json.load(open(p))
except FileNotFoundError:D={}
MAXW,MAXC,GAP=4,22,0.45
caps=[];g=[]
for i,w in enumerate(W):
    g.append([w['w'],round(w['s'],2)]);nxt=W[i+1] if i+1<len(W) else None
    chars=sum(len(x[0]) for x in g)+len(g)-1
    brk=nxt is None or len(g)>=MAXW or (w['w'][-1] in '.,?!' and len(g)>=2) or nxt['s']-w['e']>GAP or chars+1+len(nxt['w'])>MAXC
    if brk:caps.append(g);g=[]
D['caps']=caps;D['lastEnd']=round(W[-1]['e'],2)
json.dump(D,open(p,'w'))
print(len(caps),'caption groups, last word ends at',D['lastEnd'])
