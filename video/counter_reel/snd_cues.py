# Score and sound design from a list of cues in data.json ("cues"), for edits that are not the single counter shape
# (series parts, montages). Usage: python3 snd_cues.py data.json music.wav sfx.wav
# Cue types: theme [t0,t1,layers], roll [t0,t1,dip], trombone t, swell [t0,t1], hit t, groove [t0,t1,tapestop], button t,
# tension [t0,t1], sting t, impact t, boom t, aah t, buzz t (short), buzzer t, stamp t, tock t, boing t, pop t, whoosh t (end), scratch t, bell t
import json,sys,numpy as np,soundfile as sf
from synth import *
D=json.load(open(sys.argv[1]));TOTAL=D['total']/30.0;N=int(sr*(TOTAL+1.5))
music=np.zeros((N,2));sfx=np.zeros((N,2))
def theme(t0,t1,layers):
    BT=0.5;CH=[(50,[62,65,69]),(50,[61,64,69]),(43,[62,67,70]),(45,[61,64,67])]
    MEL=[[57,None,62,None,65,None,64,62],[61,None,62,None,64,None,None,None],[58,None,62,None,67,None,65,64],[64,None,61,None,57,None,None,None]]
    th=np.zeros((N,2));L1,L2,L3,L4=(list(layers)+[99,99,99,99])[:4]
    for q in range(int((t1-t0)/(BT/2))+1):
        tb=t0+q*BT/2;bar=q//8;s8=q%8;root,tri=CH[bar%4]
        if tb>=t1-0.02:break
        if s8 in(0,4):add(th,st(tuba(root if s8==0 else root+7-12*(root+7>52),BT*0.8,0.9),-0.1),tb,1.0)
        if s8 in(2,6):
            for i,m in enumerate(tri):add(th,st(pizz(m,0.55),-0.35+0.35*i),tb+0.004*i,0.9)
        if tb>=L1 and s8%2==1:add(th,st(block(1150 if s8%4==1 else 900,0.8),0.45),tb,0.55)
        m=MEL[bar%4][s8]
        if tb>=L2 and m is not None:add(th,st(reed(m,BT*0.38,0.75),0.15),tb,0.95)
        if tb>=L3:
            if m is not None:add(th,st(marimba(m+12,0.5),0.4),tb,0.55)
            add(th,st(shaker(0.7 if s8%2 else 0.4),-0.4),tb,0.35)
        if tb>=L4 and s8 in(0,4):add(th,st(kick(0.7)),tb,0.6)
    L=int((t1-t0)*sr);g=np.ones(L);g[-int(0.04*sr):]=np.linspace(1,0,int(0.04*sr));seg=th[int(t0*sr):int(t0*sr)+L]*g[:,None]
    music[int(t0*sr):int(t0*sr)+L]+=seg+0.18*reverb(seg,1.1,seed=4)[:L]
def groove(t0,t1,ts):
    B2=60/124;CH2=[(50,[66,69,74]),(47,[66,71,74]),(43,[67,71,74]),(45,[64,69,73])]
    LEAD=[[(0,81),(1,78),(1.5,81),(2.5,83)],[(0,81),(1,78),(2,76),(3,74)],[(0,79),(1,83),(1.5,81),(2.5,79)],[(0,78),(1,76),(2,73),(3,76)]]
    gr=np.zeros((N,2));end=t1+ts
    for q in range(int((end-t0)/(B2/2))+1):
        tb=t0+q*B2/2;bar=q//8;s8=q%8;root,tri=CH2[bar%4];beat=s8/2
        if tb>=end-0.01:break
        if s8 in(0,3,4):add(gr,st(kick(0.85 if s8!=3 else 0.5)),tb,0.55)
        if s8 in(2,6):add(gr,st(clap(0.9),0.05),tb,0.5)
        add(gr,st(shaker(0.6 if s8%2 else 0.35),0.35),tb,0.3);add(gr,st(shaker(0.3),0.35),tb+B2/4,0.25)
        bp={0:(root,0.6),2:(root+12,0.25),3:(root,0.3),5:(root+7,0.3),6:(root+12,0.25),7:(root+10 if bar%4==3 else root+7,0.2)}
        if s8 in bp:add(gr,st(bass(bp[s8][0]-12 if bp[s8][0]>52 else bp[s8][0],B2*bp[s8][1]*2,0.8)),tb,0.6)
        if s8 in(1,3,5,7):
            for i,m in enumerate(tri):add(gr,st(marimba(m,0.55),-0.3+0.3*i),tb+0.003*i,0.5)
        if bar%2==1 or bar>=4:
            for (bt,m) in LEAD[bar%4]:
                if abs(bt-beat)<1e-6:add(gr,st(whistle(m,B2*0.8,0.8),-0.25),tb,0.55)
    L2=int((end-t0)*sr);seg=gr[int(t0*sr):int(t0*sr)+L2].copy();g2=np.ones(L2);g2[:int(0.01*sr)]=np.linspace(0,1,int(0.01*sr))
    if ts>0:
        ts0=int((t1-t0)*sr);m_=L2-ts0;u=np.arange(m_)/sr;pos=ts0+(u-u**2/(2*ts))*sr;pos=np.clip(pos,0,L2-2);ii=pos.astype(int);fr=(pos-ii)[:,None]
        seg[ts0:]=seg[ii]*(1-fr)+seg[ii+1]*fr;g2[ts0:]*=np.linspace(1,0,m_)**0.7
    else:g2[-int(0.05*sr):]=np.linspace(1,0,int(0.05*sr))
    seg*=g2[:,None];music[int(t0*sr):int(t0*sr)+L2]+=seg+0.15*reverb(seg,1.0,seed=14)[:L2]
def tension(t0,t1):
    n=int((t1-t0)*sr);t=np.arange(n)/sr;y=np.zeros((n,2))
    for m in(38,45,50):
        for ch in(0,1):
            for dt in rng.uniform(-10,10,2):y[:,ch]+=2*((note(m)*2**(dt/1200)*t+rng.uniform())%1)-1
    fc=np.geomspace(220,900,n);y=np.stack([tvlp(y[:,0],fc,4),tvlp(y[:,1],fc,4)],1)
    e=np.clip(t/0.4,0,1)*np.clip((t1-t0-t)/0.08,0,1)*(0.55+0.45*t/max(1e-3,t1-t0));add(music,y*e[:,None],t0,0.17)
    k=0;tt=t0
    while tt<t1-0.05:
        add(music,st(block(1500 if k%2==0 else 1150,0.5),0.3 if k%2 else -0.3),tt,0.7);k+=1;tt+=0.5 if (tt-t0)<(t1-t0)*0.6 else 0.25
    add(music,st(kick(0.6)),t0,0.5)
def sting(t):
    for i,(m,d,g) in enumerate(((50,0.16,0.9),(50,0.16,0.9),(46,1.3,1.2))):
        tt=t+[0,0.2,0.42][i];n=int((d+0.4)*sr);x=np.arange(n)/sr;f=note(m);y=saw(np.full(n,f),x,14)+0.6*saw(np.full(n,f*2.003),x,10)
        env=np.clip(x/0.012,0,1)*np.exp(-x*(5 if i<2 else 1.6))*np.clip((d+0.4-x)/0.15,0,1);y=tvlp(y*env,600+2400*np.exp(-x*6),2)
        add(sfx,st(np.tanh(y*1.3)*0.5),tt,g);add(sfx,st(kick(0.9)),tt,0.7 if i<2 else 1.1)
    boomx=np.arange(int(1.6*sr))/sr;b=np.sin(2*np.pi*np.cumsum(55*np.exp(-boomx*2)+30)/sr)*np.exp(-boomx*2.5);add(sfx,st(b*0.8),t+0.42,1.0)
    tail=sfx[int(t*sr):int((t+1.0)*sr)].copy();add(sfx,0.35*reverb(tail,2.4,seed=21),t,1.0)
def impact(t):
    n=int(0.6*sr);x=np.arange(n)/n;y=bq(rng.standard_normal(n),'hp',3000)*x**3;add(sfx,st(y*0.4),t-0.6,1.0)
    bx=np.arange(int(1.2*sr))/sr;b=np.sin(2*np.pi*np.cumsum(60*np.exp(-bx*3)+32)/sr)*np.exp(-bx*3.2);add(sfx,st(np.tanh(b*1.4)*0.7),t,1.0)
    add(sfx,crash(1.0),t,0.9);add(sfx,st(kick(1.0)),t,0.8)
for c in D.get('cues',[]):
    k=c['type']
    if k=='theme':theme(c['t0'],c['t1'],c.get('layers',[c['t0']]*4))
    elif k=='roll':add(sfx,st(drumroll(c['t0'],c['t1'],duck=tuple(c['dip']) if c.get('dip') else None),0.1),c['t0'],4.0)
    elif k=='trombone':tb_=trombone(c['t']);add(sfx,st(tb_,-0.05),c['t'],1.0);add(sfx,0.2*reverb(st(tb_),1.2,seed=8),c['t'],1.0)
    elif k=='swell':sw=choir([62,66,69,74],c['t1']-c['t0']+0.05,1.0,att=c['t1']-c['t0'],pw=1.3);add(sfx,sw+0.4*reverb(sw,2.2,seed=6)[:len(sw)],c['t0'],2.8)
    elif k=='hit':
        t=c['t'];hit=choir([62,66,69,74,78],1.9,1.6,att=0.04,seed=9);hit*=np.exp(-np.arange(len(hit))/sr*1.3)[:,None];add(sfx,hit+0.5*reverb(hit,2.4,seed=12)[:len(hit)],t,2.8)
        add(sfx,bell((86,91,98),1.0),t,2.2);add(sfx,crash(1.0),t,1.8);add(sfx,st(popper(1.0),0.0),t+0.01,2.2);add(sfx,st(kick(1.0)),t,1.4)
    elif k=='aah':a=choir([62,66,69,74],0.9,1.0,att=0.08,seed=17);a*=np.exp(-np.arange(len(a))/sr*2.2)[:,None];add(sfx,a+0.4*reverb(a,1.8,seed=18)[:len(a)],c['t'],2.0);add(sfx,bell((86,91),1.0),c['t'],1.2)
    elif k=='groove':groove(c['t0'],c['t1'],c.get('tapestop',0))
    elif k=='button':
        t=c['t']
        for i,m in enumerate((62,66,69,74,78)):add(music,st(marimba(m,0.7),-0.4+0.2*i),t+0.002*i,0.8)
        add(music,st(bass(38,0.5,0.9)),t,0.7);add(sfx,crash(0.5,1.0),t,0.6);add(music,st(kick(1.0)),t,0.6)
    elif k=='tension':tension(c['t0'],c['t1'])
    elif k=='sting':sting(c['t'])
    elif k=='impact':impact(c['t'])
    elif k=='boom':
        bx=np.arange(int(1.4*sr))/sr;b=np.tanh(np.sin(2*np.pi*np.cumsum(48*np.exp(-bx*1.8)+28)/sr)*np.exp(-bx*2.2)*2.2)*0.8
        s_=st(b);add(sfx,s_,c['t'],1.2);add(sfx,0.3*reverb(s_,2.0,seed=31),c['t'],1.0)
    elif k=='buzz':add(sfx,st(buzzer(1.0)[:int(0.2*sr)]*np.linspace(1,0,int(0.2*sr))**0.5,0.0),c['t'],0.9);add(sfx,st(stamp(1.0)),c['t'],0.7)
    elif k=='buzzer':add(sfx,st(buzzer(1.0),0.0),c['t'],1.0);add(sfx,st(stamp(1.0)),c['t'],0.9)
    elif k=='tock':add(sfx,st(block(1650,1.0),0.3),c['t'],0.35)
    elif k=='boing':add(sfx,st(boing(1.0),0.2),c['t'],1.0)
    elif k=='pop':add(sfx,st(pop(1.0,c.get('f',620)),0.35),c['t'],c.get('g',1.0))
    elif k=='whoosh':add(sfx,whoosh(c.get('d',0.32),0.9),c['t']-c.get('d',0.32),1.0)
    elif k=='scratch':add(sfx,scratch(1.0,0.17),c['t'],1.0)
    elif k=='bell':add(sfx,bell(tuple(c.get('notes',(84,91))),0.7),c['t'],0.7)
music=bq(music,'lp',11000);tt=np.arange(N)/sr;sfx*=np.clip((TOTAL-tt)/0.05,0,1)[:,None];music*=np.clip((TOTAL-tt)/0.05,0,1)[:,None]
print('music peak %.3f sfx peak %.3f'%(np.abs(music).max(),np.abs(sfx).max()))
sf.write(sys.argv[2] if len(sys.argv)>2 else 'music.wav',(music[:int(TOTAL*sr)]*0.707).astype(np.float32),sr,subtype='FLOAT')
sf.write(sys.argv[3] if len(sys.argv)>3 else 'sfx.wav',(sfx[:int(TOTAL*sr)]*0.6).astype(np.float32),sr,subtype='FLOAT')
