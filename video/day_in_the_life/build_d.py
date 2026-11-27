# data.json for a story edit (worked example): cuts, captions (word times mapped from the source), pills, cards, split screen, tick list.
# Captions are typed by hand per line with the time of each word in the source file, then shifted to where the line sits in the cut.
import json,os
J=json.load(open('segs.json'));T={x['key']:x for x in J['segs']};V={v['key']:v for v in J['voice']};nf=J['nf'];END=66
# captions per voice event: groups of (word, time in the source file)
CAPT={'h1':[[('I',130.92),('was',131.00),('not',131.10)],[('expecting',131.24),('that.',131.64)]],
 'b1':[[('I',92.94),('was',93.03),('just',93.09)],[('on',93.23),('a',93.35),('walk,',93.47)],[('and',94.62),('then',94.71),('I',94.79),('heard',94.91)],[('some',95.01),('shouting.',95.19)]],
 'b2':[[('I',101.05),('was',101.17),('just',101.25),('about',101.37)],[('to',101.55),('walk',101.69),('into',101.87),('it.',102.13)]],
 'b6':[[("I'm",162.93),('gonna',163.03),('have',163.09),('to',163.17)],[('walk',163.29),('back',163.43),('now',163.61)],[('and',163.89),('get',164.89),('a',164.99),('bike.',165.11)]],
 'k2':[[('I',180.25),('told',180.73),('my',180.89),('man',181.09)],[("there's",181.31),('a',181.51),('buffalo.',181.63)]],
 'k3':[[("It's",200.87),('okay,',201.00)],[("he's",201.28),('friendly.',201.38)]],
 'k4':[[('Is',208.85),('he',209.01),('roped',209.13),('up?',209.35)]],
 'k5':[[('So',221.51),('I',221.60),('could',221.72),('have',221.84)],[('walked',221.93),('past.',222.13)],[("He's",222.42),('fine.',222.62)]],
 'z1':[[('Never',178.50),('again.',178.72)]]}
caps=[];capEnd=[]
for k in [v['key'] for v in J['voice']]:
    v=V[k];off=v['t0']-v['src'][0]
    for gi,g in enumerate(CAPT[k]):
        caps.append([[w,round(t+off,2)] for w,t in g])
        # the last group of a line clears just after the line ends, and never hangs over the next cut
        cut=min([x['e'] for x in J['segs'] if x['e']>v['t1']-0.06]);capEnd.append(round(min(v['t1']+0.12,cut-0.03),2) if gi==len(CAPT[k])-1 else None)
t=lambda k,o=0:round(T[k]['s']+o,2);e=lambda k,o=0:round(T[k]['e']+o,2);KEYS=[x['key'] for x in J['segs']]
mapn=len(os.listdir('m'));sbn=len(os.listdir('sb'))
# split screen while he is on his phone: the footage moves into a card on the left, the Maps recording grows out of his phone on the right
P0=T['p1']['s'];P1=T['p1']['e'];F=455/757.0
layouts=[{'s':round(P0+0.5,2),'e':round(P1,4),'hard':True,'x':20,'y':410,'w':455,'h':1140,'r':44,'imw':round(1080*F,1),'imx':round(-238*F,1),'imy':round(-10*F,1)}]
maps={'s':round(P0+0.55,2),'e':round(P1,4),'hard':True,'dim':False,'pop':0.3,'origin':'0% 82%','lead':0.25,'n':mapn,'dir':'m','x':499,'y':410,'w':561,'h':1140,'r':54,'bezel':True}
MAP0=maps['s']+maps['lead'];WALK=round(MAP0+1.92+0.15,2)                         # when the walking route (12 min) is on the card
sb={'s':t('w3',0.25),'e':e('w3',-0.08),'n':sbn,'dir':'sb','x':230,'y':336,'w':620,'h':1071,'r':50}
pills=[{'text':'Day in the life of an **agency owner**','s':-1,'e':e('h2',-0.03),'wipe':0.35},
 {'text':'(a buffalo got involved)','s':0.5,'e':e('h2',-0.03),'sub':True},
 {'text':'The plan: a **12 minute walk**','s':t('r1',0.17),'e':round(P1-0.02,2),'wipe':WALK},
 {'text':'Plan B: a **bike**','s':t('k1',0.09),'e':e('k2',-0.08),'wipe':t('k1',0.55)},
 {'text':'Made it. **Office for the day**','s':t('w1',0.1),'e':e('w1',-0.05),'wipe':t('w1',0.6)},
 {'text':'The actual job: **calls**','s':t('w2a',0.1),'e':e('w2',-0.05),'wipe':t('w2a',0.6)},
 {'text':'What I showed them **on the call**','s':t('w3',0.1),'e':e('w3',-0.05),'wipe':t('w3',0.65)},
 {'text':'(their ad, storyboarded)','s':t('w3',0.55),'e':e('w3',-0.05),'sub':True},
 {'text':'Call ends. **Claude** takes over','s':t('w5',0.1),'e':e('w5',-0.05),'wipe':t('w5',0.6)},
 {'text':'Easiest part of my day: **the calls**','s':t('w6',0.1),'e':e('z1',-0.03),'wipe':t('w6',0.65)},
 {'text':'(hardest part: the walk)','s':t('w6',1.0),'e':e('z1',-0.03),'sub':True}]
lists=[{'s':t('w5',0.35),'e':e('w5',-0.05),'y':292,'dim':0.22,'rows':[{'text':'Analyses the call','at':t('w5',0.95)},{'text':'Reads the transcript','at':t('w5',1.65)},{'text':'Preps my follow-up','at':t('w5',2.35)}]}]
D={'nf':nf,'total':nf+END,'vd':round(nf/30,4),'cuts':[x['s'] for x in J['segs']]+[round(nf/30,4)],'caps':caps,'capEnd':capEnd,'lastEnd':round(J['voice'][-1]['t1'],2),
   'focus':[50,42],'cutFx':{str(KEYS.index('h1')):{'zoom':0.11,'focus':[50,47]},str(KEYS.index('b2')):{'zoom':0.07,'focus':[53,62]},str(KEYS.index('k5')):{'zoom':0.10,'focus':[80,52]},str(KEYS.index('p1')):{'zoom':0.02}},'link':'stradvert.org','pills':pills,'cards':[maps,sb],'lists':lists,'layouts':layouts,'broll':[],'marks':{'map0':round(MAP0,2),'walk':WALK},'segs':{x['key']:[x['s'],x['e']] for x in J['segs']}}
json.dump(D,open('data.json','w'));print('frames',nf,'total',nf+END,round((nf+END)/30,2),'s; caption groups',len(caps))
for c,ce in zip(caps,capEnd):print('  ',c[0][1],' '.join(w for w,_ in c),'' if ce is None else f'(ends {ce})')
