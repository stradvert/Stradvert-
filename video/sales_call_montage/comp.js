/* Sales call montage, premium pass. Deterministic: render(f, sub) draws output frame f at sub-frame phase sub (0..1). */
const FPS=30,SH=0.62;let D,SCN={};
const $=id=>document.getElementById(id);
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const E={lin:x=>clamp(x),outCubic:x=>1-Math.pow(1-clamp(x),3),outQuint:x=>1-Math.pow(1-clamp(x),5),
 outExpo:x=>{x=clamp(x);return x>=1?1:1-Math.pow(2,-10*x)},inExpo:x=>{x=clamp(x);return x<=0?0:Math.pow(2,10*x-10)},
 inCubic:x=>Math.pow(clamp(x),3),inOut:x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}};
const pr=(t,s,d,e=E.outCubic)=>e((t-s)/d);
const nz=(i,t)=>Math.sin(t*1.31+i*12.9898)*.5+Math.sin(t*2.17+i*78.233)*.3+Math.sin(t*3.71+i*37.719)*.2;
const mix=(a,b,p)=>a+(b-a)*p;
const Y='#FCEF00';
const GLOW_Y='drop-shadow(0 0 10px rgba(252,239,0,.8)) drop-shadow(0 0 42px rgba(252,239,0,.5)) drop-shadow(0 0 110px rgba(252,239,0,.3))';
const GLOW_W='drop-shadow(0 0 16px rgba(255,255,255,.34)) drop-shadow(0 0 70px rgba(255,255,255,.16))';
const ROOTS=['gbg','wall','pbg','bt','stat','shadow','pfg','cap','cl','rank','chip','phones','stack','qcards','punch','hero','wtext','end3d'];
function hideAll(){ROOTS.forEach(id=>{$(id).style.display='none'});const c=$('cam');c.style.filter='none';$('flash').style.opacity=0;['o1','o2','o3','streak'].forEach(id=>$(id).style.opacity=0);$('wall').style.opacity=1;$('gbg').style.opacity=1;}
const show=(id,disp='block')=>{const e=$(id);e.style.display=disp;return e};
async function setImg(el,src){if(el.dataset.s===src)return;el.dataset.s=src;await new Promise(r=>{el.onload=r;el.onerror=()=>{console.log('IMGERR '+src);r()};el.src=src});if(el.decode){try{await el.decode()}catch(e){}}}
function ensure(el,key,html){if(el.dataset.k!==key){el.dataset.k=key;el.innerHTML=typeof html==='function'?html():html;return true}return false}
const LOOK={col:{bg:'brightness(.50) saturate(.78)',fg:'hue-rotate(8deg) brightness(1.07) contrast(1.05) saturate(.98)'},
 bw:{bg:'grayscale(1) brightness(.46) contrast(1.1)',fg:'grayscale(1) contrast(1.2) brightness(1.03)'},
 listen:{bg:'grayscale(.85) brightness(.25)',fg:'grayscale(.72) brightness(.5) contrast(1.06)'}};

/* ---------------- footage plate ---------------- */
async function footage(ctx,{z,hx,hy,look='col',dim=0,punch=0.09,exit=0,clampBg=true,bgOn=true,fgFilter=null,push=0.045,dx=0,follow=0.9}){
 const {f,lt,dur,sp,sc}=ctx;const n=String(f+1).padStart(5,'0');
 const pfg=show('pfg'),fgi=$('fgi');await setImg(fgi,'fg/'+n+'.webp');
 const pbg=$('pbg');if(bgOn){pbg.style.display='block';await setImg($('bgi'),'bg/'+n+'.jpg');}
 const box=D.fg[f]||[0,0,2,2];
 const pin=1+punch*(1-E.outExpo(lt/0.34));
 const pout=exit?1+exit*E.inExpo((lt-(dur-0.17))/0.17):1;
 const zz=z*(1+push*sp)*pin*pout;
 const tk=D.trk[f]||[sc.cx,sc.top];const cxf=mix(sc.cx,tk[0],follow),tpf=mix(sc.top,tk[1],follow);
 let tx=hx-zz*cxf+dx,ty=hy-zz*tpf;
 if(clampBg){tx=Math.min(0,Math.max(1920-1920*zz,tx));ty=Math.min(0,Math.max(1080-1080*zz,ty));}
 const tr=`translate(${tx.toFixed(2)}px,${ty.toFixed(2)}px) scale(${zz.toFixed(5)})`;
 pbg.style.transform=tr;pfg.style.transform=tr;
 fgi.style.left=box[0]+'px';fgi.style.top=box[1]+'px';fgi.style.width=box[2]+'px';fgi.style.height=box[3]+'px';
 const L=LOOK[look];
 $('bgi').style.filter=L.bg+(dim>0?` brightness(${(1-0.55*dim).toFixed(3)})`:'');
 fgi.style.filter=fgFilter||L.fg;
 return {zz,tx,ty,headX:tx+zz*cxf,headY:ty+zz*tpf};
}
/* ---------------- big type (behind subject) ---------------- */
function bigSide(el,key,txt,cls,size,at,t,{stag=0.024,dur=0.38}={}){
 const fresh=ensure(el,key,()=>`<span class="ln">${[...txt].map(c=>`<span class="ch ${c===' '?'':cls}">${c===' '?'&nbsp;':c}</span>`).join('')}</span>`);
 el.style.fontSize=size+'px';
 const chs=el.querySelectorAll('.ch');
 if(fresh||!el._m){const W=el.firstChild.offsetWidth;el._m={W,off:[...chs].map(c=>c.offsetLeft)};}
 const m=el._m,sw=pr(t,at+0.3,0.85,E.inOut),shift=mix(m.W*1.1,-m.W*2.1,sw);
 const base=cls==='gy'?'linear-gradient(180deg,#fffcbe 0%,#FCEF00 34%,#f1e300 66%,#b3a700 100%)':'linear-gradient(180deg,#ffffff 0%,#f4f4f4 46%,#c9ccd1 78%,#9da1a8 100%)';
 chs.forEach((c,i)=>{const p=pr(t,at+i*stag,dur,E.outExpo);c.style.opacity=p;
  c.style.transform=`translateY(${((1-p)*size*0.2).toFixed(2)}px) scaleY(${(1+(1-p)*0.4).toFixed(4)})`;
  c.style.filter=p<0.999?`blur(${((1-p)*size*0.05).toFixed(2)}px)`:'none';
  if(c.classList.contains(cls)){c.style.backgroundImage=`linear-gradient(104deg,rgba(255,255,255,0) 44%,rgba(255,255,255,.96) 50%,rgba(255,255,255,0) 56%),${base}`;
   c.style.backgroundSize=`${m.W*3.2}px 100%,100% 100%`;c.style.backgroundRepeat='no-repeat';c.style.backgroundPosition=`${(shift-m.off[i]).toFixed(1)}px 0,0 0`;}});
}
function bigType(ctx,{left,right,single,size,y,cls='gy',atL,atR,gx=960,gap=300,drift=1}){
 const {t,sp,sc}=ctx;const bt=show('bt');const L=$('btL'),R=$('btR');
 bt.style.filter=cls==='gy'?GLOW_Y:GLOW_W;
 const dxp=(sp-0.5)*-26*drift;
 if(single){L.style.display='block';R.style.display='none';L.style.left='0px';L.style.right='auto';L.style.width='1920px';L.style.textAlign='center';L.style.top=y+'px';
  bigSide(L,sc.key+'S',single,cls,size,atL,t);L.style.transform=`translateX(${dxp.toFixed(2)}px) scale(${(1+0.025*sp).toFixed(4)})`;}
 else{L.style.display='block';R.style.display='block';L.style.width='auto';R.style.width='auto';L.style.textAlign='right';
  L.style.left='auto';L.style.right=(1920-(gx-gap/2))+'px';L.style.top=y+'px';R.style.left=(gx+gap/2)+'px';R.style.right='auto';R.style.top=y+'px';
  bigSide(L,sc.key+'L',left,cls,size,atL,t);bigSide(R,sc.key+'R',right,cls,size,atR,t);
  L.style.transformOrigin='100% 50%';R.style.transformOrigin='0% 50%';
  L.style.transform=`translateX(${(dxp-8*sp).toFixed(2)}px) scale(${(1+0.02*sp).toFixed(4)})`;R.style.transform=`translateX(${(dxp+8*sp).toFixed(2)}px) scale(${(1+0.02*sp).toFixed(4)})`;}
}
function shadowAt(x,y,a,w=900,h=1000){const s=show('shadow');s.style.width=w+'px';s.style.height=h+'px';s.style.left=(x-w/2)+'px';s.style.top=(y-h*0.22)+'px';s.style.opacity=a;}
/* ---------------- word builders ---------------- */
function animW(nodes,items,t,{ghost=true,dur=0.22,rise=12,blur=7}={}){
 let ghosted=false;
 nodes.forEach((n,i)=>{const it=items[i];const p=pr(t,it.t-0.05,dur);
  if(p<=0){if(ghost&&!ghosted&&it.t-t<0.5){ghosted=true;n.style.opacity=0.2;n.style.filter=`blur(${blur*0.8}px)`;n.style.transform='none';}else{n.style.opacity=0;n.style.filter='none';}}
  else{n.style.opacity=p;n.style.transform=`translateY(${((1-p)*rise).toFixed(2)}px)`;n.style.filter=p<0.999?`blur(${((1-p)*blur).toFixed(2)}px)`:'none';}});
}
function caption(key,items,t,{side,x,y,em=null,alpha=1,emSize=62}){
 const el=show('cap');
 ensure(el,key,()=>items.map(it=>`<span class="w a">${it.txt}</span>`).join('')+(em?`<span class="em" style="font-size:${emSize}px">${em.map(it=>`<span class="w b">${it.txt}</span>${it.br?'<br>':''}`).join('')}</span>`:''));
 animW([...el.querySelectorAll('.w.a')],items,t);if(em)animW([...el.querySelectorAll('.w.b')],em,t,{ghost:false,dur:0.26,rise:16,blur:10});
 if(side==='L'){el.style.left='auto';el.style.right=(1920-x)+'px';el.style.textAlign='right'}else{el.style.right='auto';el.style.left=x+'px';el.style.textAlign='left'}
 el.style.top=y+'px';el.style.opacity=alpha;
}
const WI=(W,a,b)=>W.slice(a,b).map(w=>({txt:w[0],t:w[1]}));
function client(ctx,keys,{y=236}={}){
 const {t,lt,dur,sc,f}=ctx,W=sc.w;const el=show('cl');el.style.top=y+'px';el.style.left='150px';$('ctext').style.width=(ctx.cw||1010)+'px';
 const ct=$('ctext');ensure(ct,sc.key,()=>W.map((w,i)=>`<span class="w ${keys.includes(i)?'k':''}">${w[0]}</span>`).join(''));
 animW([...ct.querySelectorAll('.w')],WI(W,0,W.length),t,{dur:0.24,rise:14,blur:8});
 const p=pr(lt,0,0.34,E.outExpo),o=1-pr(lt,dur-0.1,0.1,E.lin);el.style.opacity=p*o;el.style.transform=`translateX(${((1-p)*-46).toFixed(2)}px)`;
 const e=D.env[f]||0,sh=[0.55,0.9,1,0.75,0.5];[...$('cbars').children].forEach((b,k)=>{b.style.height=(5+25*e*sh[k]*(0.72+0.28*Math.sin(f*0.9+k*1.9))).toFixed(1)+'px'});
 $('av').style.boxShadow=`0 0 0 ${(3+7*e).toFixed(1)}px rgba(252,239,0,${(0.28*e).toFixed(3)}),0 0 ${(14+30*e).toFixed(0)}px rgba(252,239,0,${(0.3+0.4*e).toFixed(3)})`;
 const g=clamp((t-W[0][1])/Math.max(0.2,sc.endsp-W[0][1]));$('clbar').style.height=(ct.offsetHeight*E.outCubic(g)+0).toFixed(1)+'px';$('clbar').style.top=($('chipc').offsetHeight+34+10)+'px';
}
/* ---------------- TV wall ---------------- */
const TV=['a','e1','b','c','f2','a2','e2','d','h','e3','b2','f'];
function buildWall(){const wc=$('wallcam');if(wc.dataset.k)return;wc.dataset.k='1';let h='';
 for(let r=0;r<3;r++)for(let c=0;c<4;c++){const i=r*4+c,x=(c-1.5)*548,y=(r-1)*436,ry=-(c-1.5)*7.5,zz=-Math.pow(Math.abs(c-1.5),2)*22;
  h+=`<div class="tv" style="transform:translate3d(${x}px,${y}px,${zz}px) rotateY(${ry}deg)"><div class="box"></div><div class="scr"><img id="tv${i}"></div><div class="lbl">CH 0${i+1>9?'':''}${i+1} &#9654;</div><div class="knob"></div><div class="led"></div></div>`;}
 wc.innerHTML=h;}
async function wallFrame(tw,{colorIdx=[5,10]}={}){buildWall();const k=Math.floor(tw*FPS);const ps=[];
 for(let i=0;i<12;i++){const im=$('tv'+i);const fr=1+((k+i*37)%166);ps.push(setImg(im,`wall/${TV[i]}/${String(fr).padStart(4,'0')}.jpg`));
  im.style.filter=colorIdx.includes(i)?'saturate(.9) contrast(1.08) brightness(.95)':'grayscale(1) contrast(1.22) brightness(.86) sepia(.18)';}
 await Promise.all(ps);}
/* ---------------- scenes ---------------- */
const S={};
S.dream=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const dim=pr(t,wt(4)-0.06,0.3);
 const fo=await footage(ctx,{z:1.5,hx:960,hy:236,dim,punch:0.14,follow:1});
 bigType(ctx,{left:'Sell you',right:'A dream',size:212,y:fo.headY+70,cls:'gy',atL:wt(4)-0.04,atR:wt(6)-0.04,gx:fo.headX+6,gap:372});
 shadowAt(fo.headX,fo.headY+120,dim*0.85);
 caption('dream',WI(W,0,4),t,{side:'L',x:fo.headX-250,y:fo.headY+118,alpha:1-pr(t,wt(4)-0.08,0.16)});
 ctx.fx.impacts=[[wt(4),0.55],[wt(7),1]];ctx.fx.fadeIn=0.12;ctx.fx.orb=[wt(4),0.7];
};
S.ask=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const fo=await footage(ctx,{z:1.16,hx:1270,hy:212,look:'bw',punch:0.07});
 caption('ask',WI(W,0,4),t,{side:'L',x:fo.headX-235,y:fo.headY+72,em:[{txt:'How',t:wt(4)},{txt:'you',t:wt(5)},{txt:'found',t:wt(6)},{txt:'us?',t:wt(7)}]});
 ctx.fx.neg=0.07;ctx.fx.rgb=[0,0.16,14];
};
S.c_found=async ctx=>{const {t,lt,dur,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const tB=wt(7)-0.16-sc.s; // local time of the cut to the card
 if(lt<tB){const out=E.inExpo((lt-(tB-0.15))/0.15);
  await footage(ctx,{z:1.3,hx:1440,hy:232,look:'listen',punch:0.06,dx:-out*700});
 }else{show('gbg');const r=show('rank'),rc=$('rankc');const l2=lt-tB;
  const p=pr(l2,0,0.42,E.outExpo);
  r.style.opacity=clamp(p*1.6);r.style.transform=`translateX(${((1-p)*520).toFixed(1)}px)`;
  rc.style.transform=`rotateY(${mix(-46,-17,p)+ctx.sp*3}deg) rotateX(${mix(14,6,p)}deg) translateZ(${ctx.sp*26}px)`;
  const q='top companies who do street polling';const nch=Math.floor(clamp((l2-0.12)/0.62)*q.length);
  $('rkq').innerHTML='&ldquo;'+q.slice(0,nch)+(nch<q.length?'<s></s>':'&rdquo;');
  const tR=wt(12)+0.12-sc.s-tB; // answer resolves as the line finishes
  [['rk1',0.5],['rk2',0.6],['rk3',0.7]].forEach(([id,s])=>{const e=$(id),pp=pr(l2,s,0.34,E.outExpo);e.style.opacity=pp;e.style.transform=`translateX(${((1-pp)*70).toFixed(1)}px)`;});
  const hi=pr(l2,tR,0.34,E.outExpo),r1=$('rk1');const sk=r1.querySelector('i'),nm=r1.querySelector('.nm');
  sk.style.display=hi>0.02?'none':'block';nm.style.display=hi>0.02?'block':'none';nm.style.opacity=hi;
  const shim=(l2*1.4)%1;[...document.querySelectorAll('.rk i')].forEach(e=>{e.style.backgroundImage=`linear-gradient(90deg,rgba(255,255,255,.2) 0%,rgba(255,255,255,.2) ${(shim*100-18).toFixed(1)}%,rgba(255,255,255,.6) ${(shim*100).toFixed(1)}%,rgba(255,255,255,.2) ${(shim*100+18).toFixed(1)}%,rgba(255,255,255,.2) 100%)`;});
  r1.style.background=hi>0?`linear-gradient(180deg,rgba(255,249,122,${hi}),rgba(252,239,0,${hi}) 45%,rgba(221,208,0,${hi}))`:'';r1.style.borderColor=hi>0?`rgba(255,251,208,${hi})`:'';
  r1.style.boxShadow=`0 0 ${70*hi}px rgba(252,239,0,${0.6*hi}),0 18px 40px rgba(0,0,0,${0.4*hi})`;r1.style.color=hi>0.5?'#111':'#fff';r1.querySelector('b').style.color=hi>0.5?'#111':'rgba(255,255,255,.75)';
  r1.querySelector('em').style.opacity=hi;r1.style.transform+=` scale(${1+0.04*hi})`;
  ctx.fx.impacts=[[sc.s+tB+tR,0.6]];ctx.fx.dots=0.3;ctx.fx.orb=[sc.s+tB,0.55];
 }
 ctx.cw=830;client(ctx,[3,7,8,11,12]);ctx.cw=0;ctx.fx.ev=[sc.s+tB,sc.s+tB+0.5];
};
S.take=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const fo=await footage(ctx,{z:1.46,hx:1300,hy:232,punch:0.12});
 caption('take',WI(W,0,8),t,{side:'L',x:fo.headX-270,y:fo.headY+150,em:[{txt:"I'll",t:wt(8)},{txt:'take',t:wt(9)},{txt:'it.',t:wt(10)}]});
 const c=show('chip'),p=pr(lt,0.04,0.45,E.outExpo);c.style.opacity=p;$('chipin').style.transform=`perspective(1100px) translateX(${((1-p)*220).toFixed(1)}px) rotateY(${mix(-38,-9,p)}deg)`;$('chipl').style.opacity=pr(lt,0.3,0.3);
 ctx.fx.flash=0.9;
};
S.c_three=async ctx=>{const {t,lt,sc,f}=ctx,W=sc.w,wt=i=>W[i][1];
 await footage(ctx,{z:1.3,hx:1440,hy:232,look:'listen',punch:0.06});
 client(ctx,[7,8]);
 const ph=show('phones');ensure(ph,'ph',()=>[0,1,2].map(i=>`<div class="ph" style="left:${i*204}px"><b>0${i+1}</b><img id="ph${i}"></div>`).join(''));
 const k=1+(Math.floor(lt*FPS)%100);await Promise.all([0,1,2].map(i=>setImg($('ph'+i),`ph/p${i+1}/${String(k).padStart(4,'0')}.jpg`)));
 [...ph.children].forEach((e,i)=>{const p=pr(t,wt(7)-0.05+i*0.09,0.4,E.outExpo);e.style.opacity=p;e.style.transform=`translateY(${((1-p)*70).toFixed(1)}px) rotateY(${mix(40,(i-1)*-9,p)}deg) rotateX(${mix(18,3,p)}deg) scale(${mix(0.8,1,p)})`;e.style.filter=p<0.99?`blur(${((1-p)*8).toFixed(1)}px)`:'none';});
 ctx.fx.ev=[wt(7)];
};
S.three=async ctx=>{const {t,lt,sc}=ctx,W=sc.w;
 const fo=await footage(ctx,{z:1.3,hx:1370,hy:222,dim:1,punch:0.12});
 const st=show('stat');ensure(st,'three',()=>`<span class="ch gy" style="display:inline-block;-webkit-background-clip:text;color:transparent;font-size:660px;letter-spacing:0">3</span><span class="ch gw" style="display:inline-block;-webkit-background-clip:text;color:transparent;font-size:176px;margin-left:34px;letter-spacing:6px">Videos</span>`);
 const [a,b]=st.children;const p1=pr(lt,0.0,0.34,E.outExpo),p2=pr(lt,0.12,0.34,E.outExpo);
 a.style.opacity=p1;a.style.transform=`translateY(${(1-p1)*90}px) scaleY(${1+(1-p1)*0.3})`;a.style.filter=`blur(${(1-p1)*24}px) ${GLOW_Y}`;
 b.style.opacity=p2;b.style.transform=`translateX(${(1-p2)*-60}px)`;b.style.filter=`blur(${(1-p2)*12}px) ${GLOW_W}`;
 shadowAt(fo.headX,fo.headY+120,0.6);ctx.fx.flash=0.8;ctx.fx.impacts=[[sc.s+0.02,0.8]];
};
S.test=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const fo=await footage(ctx,{z:1.68,hx:800,hy:236,look:'bw',punch:0.1});
 caption('test',[],t,{side:'R',x:fo.headX+400,y:fo.headY+170,emSize:84,em:[{txt:'Not',t:wt(0)},{txt:'much',t:wt(1),br:1},{txt:'to',t:wt(2)},{txt:'test.',t:wt(3)}]});
 ctx.fx.neg=0.07;
};
S.c_ten=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 await footage(ctx,{z:1.3,hx:1440,hy:232,look:'listen',punch:0.06});
 client(ctx,[2,3]);
 show('stack');const sc2=$('stackc');ensure(sc2,'st',()=>Array.from({length:10},(_,k)=>`<div class="slab ${k===9?'top':''}">${[4,3,2,1].map(j=>`<div class="e" style="transform:translateZ(${-j*3}px)"></div>`).join('')}<div class="f"></div></div>`).join(''));
 const t0=wt(2)-0.05;let cnt=0;
 [...sc2.children].forEach((e,k)=>{const p=pr(t,t0+k*0.062,0.34,E.outExpo);if(p>0.5)cnt=k+1;e.style.opacity=clamp((p-0.25)*2.2);e.style.transform=`translateZ(${(k*30+(1-p)*300).toFixed(1)}px) rotateZ(${((1-p)*24+((k*37)%7-3)*1.4).toFixed(2)}deg)`;});
 const sn=$('stackn');sn.innerHTML=`${cnt}<small>questions</small>`;sn.style.opacity=pr(t,t0,0.2);sn.style.transform=`scale(${1+0.08*(1-pr(t,t0+Math.max(0,cnt-1)*0.062,0.12))})`;
 ctx.fx.ev=[t0,t0+0.3,t0+0.6];
};
S.street=async ctx=>{const {t,lt,dur,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 show('wall');await wallFrame(lt);
 const a=E.outCubic(lt/1.5),zin=E.inExpo((lt-(dur-0.24))/0.24);
 const dz=mix(-1150,-330,a)+zin*1500,ry=mix(-24,-5,a)*(1-zin),rx=mix(9,3,a)*(1-zin),px=mix(-70,50,a)*(1-zin),py=mix(60,-10,a);
 $('wallcam').style.transform=`translateZ(${dz.toFixed(1)}px) rotateX(${rx.toFixed(3)}deg) rotateY(${ry.toFixed(3)}deg) translate3d(${(-px).toFixed(1)}px,${(-py).toFixed(1)}px,0)`;
 show('wtext');const ws=$('wsmall');ensure(ws,'ws',()=>W.slice(0,6).map(w=>`<span class="w">${w[0]}</span>`).join(''));animW([...ws.children],WI(W,0,6),t);
 ws.style.opacity=1-pr(t,wt(6)+0.1,0.2);
 const wb=$('wbig');ensure(wb,'wb',()=>['Street','Interviews'].map(l=>`<span class="l">${[...l].map(c=>`<span class="ch gw">${c}</span>`).join('')}</span>`).join(''));
 wb.style.filter=GLOW_W;wb.style.transform=`rotateY(${mix(-9,3,ctx.sp)}deg) rotateX(2deg) scale(${(1+0.05*ctx.sp+zin*1.2).toFixed(4)})`;wb.style.opacity=1-zin;
 [...wb.children].forEach((l,li)=>{[...l.children].forEach((c,i)=>{const p=pr(t,wt(6+li)-0.05+i*0.02,0.36,E.outExpo);c.style.opacity=p;c.style.transform=`translateY(${((1-p)*46).toFixed(1)}px) skewX(${((1-p)*-14).toFixed(2)}deg)`;c.style.filter=p<0.999?`blur(${((1-p)*14).toFixed(1)}px)`:'none';});});
 ctx.fx.dots=0.34;ctx.fx.orbs=true;ctx.fx.impacts=[[wt(6),0.5],[wt(7),0.8]];ctx.fx.ev=[sc.s,wt(6),wt(7),sc.e-0.24,sc.e-0.1];ctx.fx.flashEnd=0.24;ctx.fx.noshake=zin>0;
};
S.follow=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const fo=await footage(ctx,{z:1.4,hx:1420,hy:232,punch:0.28});
 show('qcards');[['qc1',wt(3)],['qc2',wt(6)]].forEach(([id,s],i)=>{const e=$(id),p=pr(t,s-0.06,0.46,E.outExpo);e.style.opacity=clamp(p*1.4);
  e.style.transform=`translateX(${((1-p)*-120).toFixed(1)}px) rotateY(${mix(64,13,p)-ctx.sp*3}deg) rotateX(${mix(8,2,p)}deg)`;e.style.filter=p<0.99?`blur(${((1-p)*10).toFixed(1)}px)`:'none';});
 caption('follow',[],t,{side:'R',x:156,y:670,em:[{txt:"That's",t:wt(7)},{txt:'about',t:wt(8)},{txt:'it.',t:wt(9)}]});
 ctx.fx.flash=1;ctx.fx.impacts=[[wt(3),0.45],[wt(6),0.45]];ctx.fx.ev=[wt(3),wt(6),wt(7)];
};
S.c_org=async ctx=>{const {sc}=ctx;await footage(ctx,{z:1.3,hx:1440,hy:232,look:'listen',punch:0.06});client(ctx,[6,7]);};
S.conv=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const dim=pr(t,wt(6)-0.06,0.3);
 const fo=await footage(ctx,{z:1.42,hx:960,hy:250,dim,punch:0.12,follow:1});
 bigType(ctx,{single:'Conversion',size:428,y:fo.headY-6,cls:'gw',atL:wt(6)-0.04});
 shadowAt(fo.headX,fo.headY+140,dim*0.8);
 caption('conv',WI(W,0,6),t,{side:'R',x:fo.headX+270,y:fo.headY+128,alpha:1-pr(t,wt(6)-0.08,0.16)});
 ctx.fx.flash=0.8;ctx.fx.impacts=[[wt(6),1]];ctx.fx.orb=[wt(6),0.6];ctx.fx.ev=[wt(6)];
};
S.c_plain=async ctx=>{const {t,lt,sc,f}=ctx,W=sc.w,wt=i=>W[i][1];
 const cuts=[sc.s,wt(4)-0.04,wt(9)-0.04];let pi=0;cuts.forEach((c,i)=>{if(t>=c-1e-4)pi=i});
 const P=[{z:1.2,hx:1180,hy:150,a:0,b:4,k:[3]},{z:1.42,hx:760,hy:110,a:4,b:9,k:[]},{z:1.62,hx:980,hy:60,a:9,b:13,k:[11,12]}][pi];
 const l2=t-cuts[pi];
 // local punch per phrase
 const c2={...ctx,lt:l2};await footage(c2,{z:P.z,hx:P.hx,hy:P.hy,look:'bw',punch:0.1,push:0.02});
 $('bgi').style.filter='grayscale(1) brightness(.3) contrast(1.1)';$('fgi').style.filter='grayscale(1) contrast(1.22) brightness(.82)';
 const pu=show('punch');ensure(pu,'p'+pi,()=>W.slice(P.a,P.b).map((w,i)=>`<span class="w ${P.k.includes(P.a+i)?'k':''}">${w[0]}</span>`).join(''));
 animW([...pu.children],WI(W,P.a,P.b),t,{ghost:false,dur:0.2,rise:20,blur:12});
 pu.style.top='842px';
 const cl=show('cl');cl.style.top='950px';cl.style.left='780px';$('ctext').innerHTML='';$('ctext').dataset.k='';$('clbar').style.height='0px';cl.style.opacity=1;cl.style.transform='none';
 const e=D.env[f]||0,sh=[0.55,0.9,1,0.75,0.5];[...$('cbars').children].forEach((b,k)=>{b.style.height=(5+25*e*sh[k]*(0.72+0.28*Math.sin(f*0.9+k*1.9))).toFixed(1)+'px'});
 ctx.fx.neg=l2<0.07?0.07:0;ctx.fx.negLocal=l2;ctx.fx.ev=cuts;
};
S.prob=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 show('gbg');
 const duo='contrast(1.22) brightness(1.06) url(#duo) drop-shadow(0 0 34px rgba(252,239,0,.3))';
 await footage(ctx,{z:1.36,hx:520,hy:196,clampBg:false,bgOn:false,fgFilter:duo,punch:0.1});
 const h=show('hero');ensure(h,'hero',()=>`<div class="q">&ldquo;</div><div class="s s1">${W.slice(0,5).map(w=>`<span class="w">${w[0]}</span>`).join('')}</div><div class="big">${[...'The problem'].map(c=>`<span class="ch ${c===' '?'':'gw'}">${c===' '?'&nbsp;':c}</span>`).join('')}</div><div class="s s2">${W.slice(7,10).map(w=>`<span class="w">${w[0]}</span>`).join('')}</div><div class="tm"><div class="y">Them &#10003;</div><div class="n"><span>Me</span></div></div>`);
 animW([...h.querySelectorAll('.s1 .w')],WI(W,0,5),t);animW([...h.querySelectorAll('.s2 .w')],WI(W,7,10),t);
 const big=h.querySelector('.big');big.style.filter=GLOW_W;
 const chs=[...big.children];if(!big._m){big._m={W:big.offsetWidth,off:chs.map(c=>c.offsetLeft)};}
 const at=wt(5)-0.04,sw=pr(t,at+0.35,0.8,E.inOut),shift=mix(big._m.W*1.1,-big._m.W*2.1,sw);
 chs.forEach((c,i)=>{const p=pr(t,at+i*0.024,0.38,E.outExpo);c.style.opacity=p;c.style.transform=`translateY(${((1-p)*44).toFixed(1)}px) scaleY(${(1+(1-p)*0.4).toFixed(3)})`;c.style.filter=p<0.999?`blur(${((1-p)*11).toFixed(1)}px)`:'none';
  if(c.classList.contains('gw')){c.style.backgroundImage=`linear-gradient(104deg,rgba(255,255,255,0) 44%,rgba(255,255,255,.96) 50%,rgba(255,255,255,0) 56%),linear-gradient(180deg,#ffffff 0%,#f4f4f4 46%,#c9ccd1 78%,#9da1a8 100%)`;c.style.backgroundSize=`${big._m.W*3.2}px 100%,100% 100%`;c.style.backgroundRepeat='no-repeat';c.style.backgroundPosition=`${(shift-big._m.off[i]).toFixed(1)}px 0,0 0`;}});
 const q=h.querySelector('.q'),qp=pr(lt,0.05,0.4,E.outExpo);q.style.opacity=qp;q.style.transform=`translateY(${(1-qp)*-30}px)`;
 const tm=h.querySelector('.tm');[...tm.children].forEach((e,i)=>{const p=pr(t,(i===0?wt(3)+0.25:wt(9)-0.05),0.36,E.outExpo);e.style.opacity=p;e.style.transform=`translateY(${(1-p)*26}px)`;});
 $('arc').style.transform=`rotate(${ctx.sp*10}deg)`;
 ctx.fx.neg=0.07;ctx.fx.dots=0.3;ctx.fx.impacts=[[wt(5),0.8]];ctx.fx.orb=[wt(5),0.5];ctx.fx.ev=[wt(5),wt(7),wt(9)];
};
S.one=async ctx=>{const {t,lt,sc}=ctx,W=sc.w,wt=i=>W[i][1];
 const dim=pr(t,wt(12)-0.06,0.3);
 const fo=await footage(ctx,{z:1.4,hx:1190,hy:250,dim,punch:0.12,follow:1});
 bigType(ctx,{left:'Number',right:'One',size:280,y:fo.headY+34,cls:'gy',atL:wt(12)-0.04,atR:wt(13)-0.04,gx:fo.headX+4,gap:380});
 shadowAt(fo.headX,fo.headY+130,dim*0.85);
 if(t<wt(7)-0.04)caption('oneA',WI(W,0,7),t,{side:'L',x:fo.headX-270,y:fo.headY+140,alpha:1-pr(t,wt(7)-0.14,0.1)});
 else caption('oneB',WI(W,7,12),t,{side:'L',x:fo.headX-270,y:fo.headY+140,alpha:1-pr(t,wt(12)-0.08,0.16)});
 ctx.fx.flash=0.8;ctx.fx.impacts=[[wt(12),0.7],[wt(13),1.2]];ctx.fx.orb=[wt(12),0.75];ctx.fx.ev=[wt(7),wt(12),wt(13)];
};
/* ---------------- end card ---------------- */
async function endCard(ctx){const {t}=ctx;const l=t-D.vd;
 const w=show('wall');w.style.opacity=0.34;await wallFrame(l+3,{colorIdx:[]});
 $('wallcam').style.transform=`translateZ(${(-1500+l*40).toFixed(1)}px) rotateX(5deg) rotateY(${(-10+l*3).toFixed(2)}deg) translate3d(0,-60px,0)`;
 show('end3d');const ex=$('ex');const N=30;
 ensure(ex,'ex',()=>{let h=`<span style="transform:translateZ(-70px);color:#FCEF00;filter:blur(46px);opacity:.75">stradvert.org</span>`;
  for(let i=N-1;i>=1;i--){const k=i/(N-1),c=`rgb(${Math.round(mix(196,84,k))},${Math.round(mix(186,78,k))},0)`;h+=`<span style="transform:translateZ(${(-i*1.7).toFixed(1)}px);color:${c}">stradvert.org</span>`;}
  h+=`<span id="exr" style="color:#FCEF00;opacity:.2;filter:blur(3px);-webkit-mask-image:linear-gradient(to top,rgba(0,0,0,.9),rgba(0,0,0,0) 62%);mask-image:linear-gradient(to top,rgba(0,0,0,.9),rgba(0,0,0,0) 62%)">stradvert.org</span>`;
  h+=`<span id="exf" style="-webkit-background-clip:text;background-clip:text;color:transparent">stradvert.org</span>`;return h;});
 if(!ex._w){const f=$('exf');ex._w=f.offsetWidth;ex._h=f.offsetHeight;[...ex.children].forEach(s=>{s.style.marginLeft=(-ex._w/2)+'px';s.style.marginTop=(-ex._h/2)+'px'});$('exr').style.transform=`translateY(${(ex._h*0.74).toFixed(1)}px) scaleY(-1)`;$('endshadow').textContent='stradvert.org';}
 const p=pr(l,0.0,0.7,E.outExpo),ry=mix(-34,-13,p)+l*3.2,rx=mix(16,7,p);
 ex.style.transform=`translateZ(${mix(-700,0,p).toFixed(1)}px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg)`;ex.style.opacity=clamp(p*1.8);
 const sw=pr(l,0.75,0.9,E.inOut);$('exf').style.backgroundImage=`linear-gradient(104deg,rgba(255,255,255,0) 44%,rgba(255,255,255,.98) 50%,rgba(255,255,255,0) 56%),linear-gradient(180deg,#fffdc8 0%,#FCEF00 36%,#efe100 68%,#c2b600 100%)`;
 $('exf').style.backgroundSize=`${ex._w*3.2}px 100%,100% 100%`;$('exf').style.backgroundRepeat='no-repeat';$('exf').style.backgroundPosition=`${mix(ex._w*1.1,-ex._w*2.1,sw).toFixed(1)}px 0,0 0`;
 const fl=$('endfloor');fl.style.transform=`rotateX(74deg)`;fl.style.opacity=p;
 const sh=$('endshadow');sh.style.transform=`translateX(-50%) rotateX(74deg) rotateZ(${(-ry*0.25).toFixed(2)}deg) scaleY(1.5)`;sh.style.opacity=0.7*p;
 const lg=$('logo'),lp=pr(l,0.3,0.5,E.outExpo);lg.style.opacity=lp;lg.style.transform=`translateY(${((1-lp)*-24).toFixed(1)}px) scale(${mix(0.92,1,lp)})`;
 const es=$('endsub'),sp2=pr(l,0.62,0.5);es.style.opacity=sp2;es.style.letterSpacing=mix(18,9,sp2).toFixed(2)+'px';
 ctx.fx.flash=0.95;ctx.fx.dots=0.26;ctx.fx.impacts=[[D.vd+0.03,1.1]];ctx.fx.orb=[D.vd+0.1,0.6];ctx.fx.notag=1;ctx.fx.streak=[D.vd+0.75,0.9];
}
/* ---------------- frame ---------------- */
function sceneOf(f){let i=0;D.sc.forEach((s,k)=>{if(f>=s.f0)i=k});return D.sc[i]}
window.samples=function(f){if(f>=D.nf)return (f-D.nf)<26?6:3;const sc=sceneOf(f),t=f/FPS;
 const ev=[sc.s,...(SCN[sc.key]||[])];let hot=ev.some(e=>t-e>-0.05&&t-e<0.46)||sc.e-t<0.2;return hot?6:2;};
window.render=async function(f,sub=0){
 const t=(f+sub*SH)/FPS;hideAll();
 const ctx={f,t,fx:{}};let sc=null;
 if(f>=D.nf){await endCard(ctx);ctx.lt=t-D.vd;ctx.sStart=D.vd;}
 else{sc=sceneOf(f);ctx.sc=sc;ctx.lt=Math.max(0,t-sc.s);ctx.dur=sc.e-sc.s;ctx.sp=clamp(ctx.lt/ctx.dur);ctx.sStart=sc.s;await S[sc.key](ctx);}
 const fx=ctx.fx,lt=ctx.lt;
 // camera: handheld drift + impact shake
 let sx=nz(1,t)*2.6,sy=nz(2,t)*2.0,rot=nz(3,t)*0.11;
 (fx.impacts||[]).forEach(([ti,a])=>{const d=t-ti;if(d>=0&&d<0.5){const k=a*15*Math.exp(-d*10);sx+=k*Math.sin(d*96+1.3);sy+=k*Math.cos(d*83+0.4);}});
 if(fx.noshake){sx=sy=rot=0;}
 let filt='';
 if(fx.rgb){const [a,b,amp]=fx.rgb;if(lt>=a&&lt<b){const k=amp*(1-(lt-a)/(b-a));$('fo1').setAttribute('dx',k.toFixed(1));$('fo2').setAttribute('dx',(-k).toFixed(1));filt+='url(#rgb) ';}}
 const negL=fx.negLocal!==undefined?fx.negLocal:lt;if(fx.neg&&negL<fx.neg)filt+='invert(1) grayscale(1) contrast(1.15) ';
 const cam=$('cam');cam.style.filter=filt||'none';cam.style.transform=`translate(${sx.toFixed(2)}px,${sy.toFixed(2)}px) rotate(${rot.toFixed(4)}deg) scale(1.012)`;
 // flash + fades
 let fl=0;if(fx.flash)fl=Math.max(fl,fx.flash*Math.exp(-lt*13));if(fx.flashEnd&&sc){fl=Math.max(fl,E.inExpo((lt-(ctx.dur-fx.flashEnd))/fx.flashEnd)*0.9);}
 const F=$('flash');F.style.background='#fff';F.style.opacity=fl.toFixed(4);
 if(fx.fadeIn&&lt<fx.fadeIn){F.style.background='#000';F.style.opacity=(1-lt/fx.fadeIn).toFixed(4);}
 // light orbs
 const orbs=[];if(fx.orb){const [ti,a]=fx.orb;const d=t-ti;if(d>-0.1&&d<1.3){const k=a*Math.exp(-Math.max(0,d)*2.6)*clamp((d+0.1)/0.12);orbs.push([mix(-300,1500,clamp(d/1.3)),-260+d*120,k]);}}
 if(fx.orbs){const l=lt;orbs.push([mix(1500,-400,clamp(l/2.2)),40,0.34],[mix(-500,900,clamp(l/2.6)),420,0.22]);}
 ['o1','o2','o3'].forEach((id,i)=>{const o=$(id);if(orbs[i]){o.style.opacity=orbs[i][2].toFixed(3);o.style.transform=`translate(${orbs[i][0].toFixed(1)}px,${orbs[i][1].toFixed(1)}px)`;}else o.style.opacity=0;});
 if(fx.streak){const [ti,a]=fx.streak;const d=t-ti;const st=$('streak');if(d>0&&d<0.9){st.style.opacity=(a*Math.sin(Math.PI*d/0.9)).toFixed(3);st.style.top=(545+d*10)+'px';st.style.transform=`scaleX(${(0.3+d*1.1).toFixed(3)})`;}}
 $('dots').style.opacity=(fx.dots!==undefined?fx.dots:0.10);
 $('tag').style.opacity=fx.notag?0:1;
};
window.ready=(async()=>{D=await (await fetch('data.json')).json();
 // event times for adaptive motion-blur sampling
 const g=k=>D.sc.find(s=>s.key===k),w=(k,i)=>g(k).w[i][1];
 SCN={dream:[w('dream',4),w('dream',6)],ask:[w('ask',4)],c_found:[w('c_found',7)-0.3,w('c_found',7)-0.16,w('c_found',12)],take:[w('take',8)],c_three:[w('c_three',7)],three:[],test:[w('test',0)],
  c_ten:[w('c_ten',2),w('c_ten',2)+0.4],street:[w('street',6),w('street',7),g('street').e-0.3],follow:[w('follow',3),w('follow',6),w('follow',7)],c_org:[],conv:[w('conv',6)],
  c_plain:[w('c_plain',4),w('c_plain',9)],prob:[w('prob',5),w('prob',7),w('prob',9)],one:[w('one',7),w('one',12),w('one',13)]};
 for(const f of['400 60px A','500 60px AX','italic 500 60px AX','800 60px AX','italic 800 60px AX','italic 900 60px AX','italic 900 60px MI'])await document.fonts.load(f);await document.fonts.ready;})();
