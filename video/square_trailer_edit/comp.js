/* Square edit inside a 1080x1920 portrait canvas (the square is #stage, 1080x1080). Deterministic: render(f, sub) draws output frame f at sub-frame phase sub (0..1). */
const FPS=30,SH=0.62,SW=1080;let D,EV={};
const $=id=>document.getElementById(id);
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const E={lin:x=>clamp(x),outCubic:x=>1-Math.pow(1-clamp(x),3),outQuint:x=>1-Math.pow(1-clamp(x),5),
 outExpo:x=>{x=clamp(x);return x>=1?1:1-Math.pow(2,-10*x)},inExpo:x=>{x=clamp(x);return x<=0?0:Math.pow(2,10*x-10)},
 inOut:x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}};
const pr=(t,s,d,e=E.outCubic)=>e((t-s)/d);
const nz=(i,t)=>Math.sin(t*1.31+i*12.9898)*.5+Math.sin(t*2.17+i*78.233)*.3+Math.sin(t*3.71+i*37.719)*.2;
const mix=(a,b,p)=>a+(b-a)*p;
const GLOW_Y='drop-shadow(0 0 10px rgba(252,239,0,.8)) drop-shadow(0 0 40px rgba(252,239,0,.5)) drop-shadow(0 0 100px rgba(252,239,0,.3))';
const GLOW_W='drop-shadow(0 0 14px rgba(255,255,255,.34)) drop-shadow(0 0 60px rgba(255,255,255,.16)) drop-shadow(0 4px 18px rgba(0,0,0,.5))';
const GY='linear-gradient(180deg,#fffcbe 0%,#FCEF00 34%,#f1e300 66%,#b3a700 100%)',GW='linear-gradient(180deg,#ffffff 0%,#f4f4f4 46%,#c9ccd1 78%,#9da1a8 100%)';
const ROOTS=['gbg','pvbg','wall','pbg','scan','scan2','bt','rows','stat','shadow','strike','pfg','vf','cards','chart','aichip','real','phone','pip','chips','scrim','cap','end3d'];
function hideAll(){ROOTS.forEach(id=>{$(id).style.display='none'});$('cam').style.filter='none';$('flash').style.opacity=0;['o1','o2','o3','streak'].forEach(id=>$(id).style.opacity=0);$('wall').style.opacity=1;}
const show=(id,disp='block')=>{const e=$(id);e.style.display=disp;return e};
const pad=(n,k=5)=>String(n).padStart(k,'0');
async function setImg(el,src){if(el.dataset.s===src)return;el.dataset.s=src;await new Promise(r=>{el.onload=r;el.onerror=()=>{console.log('IMGERR '+src);r()};el.src=src});if(el.decode){try{await el.decode()}catch(e){}}}
function ensure(el,key,html){if(el.dataset.k!==key){el.dataset.k=key;el.innerHTML=typeof html==='function'?html():html;el._m=null;return true}return false}
const norm=s=>s.toLowerCase().replace(/[^a-z0-9%€']/g,'');
function T(sc,word,nth=0){let k=0;for(const w of sc.w){if(norm(w[0])===norm(word)){if(k===nth)return w[1];k++}}console.log('IMGERR missing word '+word+' in '+sc.key);return sc.s}

/* ---------------- footage plate ---------------- */
async function plate(ctx,{z=1,hx=800,dim=0,focus=0,punch=0.06,push=0.03,follow=0.9,fgFilter=null,fgOn=true,dx=0}={}){
 const {f,sp,sc,ls}=ctx;const n=pad(f+1);
 show('pbg');await setImg($('bgi'),'bgs/'+n+'.jpg');
 const bb=$('bgb');if(focus>0.01){bb.style.display='block';await setImg(bb,'bgm/'+n+'.jpg');bb.style.opacity=clamp(focus)}else bb.style.display='none';
 $('fk').style.display='none';
 const pfg=$('pfg'),fgi=$('fgi');if(fgOn){pfg.style.display='block';await setImg(fgi,'fg/'+n+'.webp');}
 const box=D.fg[f]||[0,0,2,2];
 const pin=1+punch*(1-E.outExpo(ls/0.34));
 const zz=z*(1+push*sp)*pin;
 const tk=D.trk[f]||[sc.cx,sc.top];const cxf=mix(sc.cx,tk[0],follow),tpf=mix(sc.top,tk[1],follow);
 let tx=hx-zz*cxf+dx,ty=-(zz-1)*(tpf+230);
 tx=Math.min(0,Math.max(SW-1920*zz,tx));ty=Math.min(0,Math.max(SW-1080*zz,ty));
 const tr=`translate(${tx.toFixed(2)}px,${ty.toFixed(2)}px) scale(${zz.toFixed(5)})`;
 $('pbg').style.transform=tr;pfg.style.transform=tr;
 fgi.style.left=box[0]+'px';fgi.style.top=box[1]+'px';fgi.style.width=box[2]+'px';fgi.style.height=box[3]+'px';
 fgi.style.filter=fgFilter||(sc.look==='int'?'brightness(1.02) contrast(1.03)':'brightness(1.04) contrast(1.04) saturate(1.03)');
 $('sky').style.background=sc.look==='int'?'linear-gradient(90deg,rgba(14,22,40,.30) 0%,rgba(14,22,40,.10) 45%,rgba(14,22,40,0) 70%)':'linear-gradient(180deg,rgba(14,28,56,.30) 0%,rgba(14,28,56,.12) 26%,rgba(14,28,56,0) 46%)';
 $('dim').style.opacity=clamp(dim);
 return {zz,tx,ty,headX:tx+zz*cxf,headY:ty+zz*tpf};
}
/* ---------------- big type line ---------------- */
function typeLine(el,key,txt,cls,size,at,t,{stag=0.024,dur=0.38,sweep=true}={}){
 ensure(el,key,()=>`<span class="ln">${[...txt].map(c=>`<span class="ch ${c===' '?'':cls}">${c===' '?'&nbsp;':c}</span>`).join('')}</span>`);
 el.style.fontSize=size+'px';const chs=el.querySelectorAll('.ch');
 if(!el._m){el._m={W:el.firstChild.offsetWidth,off:[...chs].map(c=>c.offsetLeft)};}
 const m=el._m,sw=sweep?pr(t,at+0.3,0.85,E.inOut):0,shift=mix(m.W*1.1,-m.W*2.1,sw),base=cls==='gy'?GY:GW;
 chs.forEach((c,i)=>{const p=pr(t,at+i*stag,dur,E.outExpo);c.style.opacity=p;
  c.style.transform=`translateY(${((1-p)*size*0.2).toFixed(2)}px) scaleY(${(1+(1-p)*0.4).toFixed(4)})`;
  c.style.filter=p<0.999?`blur(${((1-p)*size*0.05).toFixed(2)}px)`:'none';
  if(c.classList.contains(cls)){c.style.backgroundImage=`linear-gradient(104deg,rgba(255,255,255,0) 44%,rgba(255,255,255,.96) 50%,rgba(255,255,255,0) 56%),${base}`;
   c.style.backgroundSize=`${m.W*3.2}px 100%,100% 100%`;c.style.backgroundRepeat='no-repeat';c.style.backgroundPosition=`${(shift-m.off[i]).toFixed(1)}px 0,0 0`;}});
 return m.W;
}
function shadowAt(x,y,a,w=820,h=900){const s=show('shadow');s.style.width=w+'px';s.style.height=h+'px';s.style.left=(x-w/2)+'px';s.style.top=(y-h*0.2)+'px';s.style.opacity=a;}
const pop=(el,t,at,{dur=0.4,dy=24,blur=8,e=E.outExpo}={})=>{const p=pr(t,at,dur,e);el.style.opacity=p;el.style.transform=`translateY(${((1-p)*dy).toFixed(2)}px)`;el.style.filter=p<0.999?`blur(${((1-p)*blur).toFixed(2)}px)`:'none';return p};
/* ---------------- captions ---------------- */
function captions(ctx){const {t,sc}=ctx;let g=null;for(const c of D.caps){if(c.sc===sc.key&&t>=c.s-0.04&&t<c.e){g=c}}
 if(!g)return;const el=show('cap');show('scrim');
 ensure(el,sc.key+g.a,()=>sc.w.slice(g.a,g.b).map(w=>`<span class="w ${w[2]?'k':''}">${w[0]}</span>`).join(''));
 let ghosted=false;[...el.children].forEach((n,i)=>{const w=sc.w[g.a+i];const p=pr(t,w[1]-0.05,0.2);
  if(p<=0){if(!ghosted&&w[1]-t<0.45){ghosted=true;n.style.opacity=0.22;n.style.filter='blur(4px)';n.style.transform='none'}else{n.style.opacity=0;n.style.filter='none'}}
  else{n.style.opacity=p;n.style.transform=`translateY(${((1-p)*12).toFixed(2)}px)`;n.style.filter=p<0.999?`blur(${((1-p)*6).toFixed(2)}px)`:'none'}});
 el.style.opacity=(1-pr(t,g.e-0.07,0.07,E.lin)).toFixed(3);
}
/* ---------------- TV wall (end card backdrop) ---------------- */
const TV=['c','e1','c2','e2','f2','e3','d2','f','d'];   // 3 x 3; same-shoot clips never side by side (the centre tile sits under the URL)
function buildWall(){const wc=$('wallcam');if(wc.dataset.k)return;wc.dataset.k='1';let h='';
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){const i=r*3+c,x=(c-1)*548,y=(r-1)*436,ry=-(c-1)*7.5,zz=-Math.pow(Math.abs(c-1),2)*22;
  h+=`<div class="tv" style="transform:translate3d(${x}px,${y}px,${zz}px) rotateY(${ry}deg)"><div class="box"></div><div class="scr"><img id="tv${i}"></div><div class="lbl">CH ${i+1} &#9654;</div><div class="knob"></div><div class="led"></div></div>`;}
 wc.innerHTML=h;}
async function wallFrame(tw){buildWall();const k=Math.floor(tw*FPS);const ps=[];
 for(let i=0;i<TV.length;i++){const im=$('tv'+i);const fr=1+((k+i*37)%166);ps.push(setImg(im,`wall/${TV[i]}/${pad(fr,4)}.jpg`));im.style.filter='grayscale(1) contrast(1.22) brightness(.86) sepia(.18)';}
 await Promise.all(ps);}
/* ---------------- scenes ---------------- */
const S={};
S.hook=async ctx=>{const {t,lt,sc,sp}=ctx;const tn=T(sc,'never'),tv=T(sc,'view');
 const pan=pr(t,tv-0.3,0.8,E.inOut),dn=pr(t,tn-0.05,0.25)*(1-pr(t,tv-0.45,0.3));
 const fo=await plate(ctx,{z:1.0,hx:mix(860,950,pan),dim:0.30*dn,focus:0.75*dn,punch:0.1});
 const bt=show('bt');bt.style.left='44px';bt.style.top='150px';bt.style.filter=GLOW_Y;typeLine(bt,'hk','Never','gy',230,tn-0.04,t);
 bt.style.opacity=(1-pr(t,tv-0.45,0.22)).toFixed(3);bt.style.transform=`scale(${(1+0.03*sp).toFixed(4)})`;bt.style.transformOrigin='0 50%';
 shadowAt(fo.headX,fo.headY+200,dn*0.8);
 const vf=show('vf'),p=pr(t,tv-0.22,0.45,E.outExpo);vf.style.opacity=p;vf.style.transform=`scale(${mix(1.22,1,p).toFixed(4)})`;
 vf.querySelector('b').style.transform=`scale(${(1+0.25*Math.sin((t-tv)*9)).toFixed(3)})`;vf.querySelector('b').style.opacity=clamp((t-tv)*4);
 ctx.fx.impacts=[[tn,0.9]];ctx.fx.orb=[tn,0.55];ctx.fx.vig=0.8;
};
S.reason=async ctx=>{const {t,lt,sc,sp}=ctx;const t1=T(sc,'polished'),t2=T(sc,'prepared'),t3=T(sc,'fake'),tl=T(sc,'more',0)-0.36;
 const dn=pr(t,tl,0.5);
 const fo=await plate(ctx,{z:1.03,hx:872,dim:0.34*dn,focus:0.8*dn,punch:0.08});
 const rw=show('rows');rw.style.top='120px';const lab=$('rlab'),lab2=$('rlab2');lab.style.display='block';lab.textContent='The more';lab.style.top='0px';pop(lab,t,tl,{dy:14});
 [['row1',t1,50,116,'Polished','gw'],['row2',t2,176,116,'Prepared','gw'],['row3',t3,348,250,'Fake','gy']].forEach(([id,at,top,size,txt,cls])=>{const r=$(id);r.style.display='block';r.style.transform='none';r.style.top=top+'px';r.style.filter=cls==='gy'?GLOW_Y:GLOW_W;typeLine(r,'rs'+id,txt,cls,size,at-0.04,t);});
 lab2.style.display='block';lab2.style.top='306px';pop(lab2,t,T(sc,'more',2)-0.3,{dy:14});
 rw.style.transform=`translateX(${((sp-0.5)*-14).toFixed(2)}px)`;
 shadowAt(fo.headX,fo.headY+200,dn*0.8);
 ctx.fx.flash=0.5;ctx.fx.impacts=[[t1,0.35],[t2,0.35],[t3,1.1]];ctx.fx.orb=[t3,0.6];ctx.fx.vig=0.8;
};
function statBlock(key,html){const st=show('stat');ensure(st,key,html);return st}
const fmt=n=>Math.round(n).toLocaleString('en-US');
S.proof=async ctx=>{const {t,lt,sc,sp,shot}=ctx;const tm=T(sc,'my'),tnm=T(sc,'€000,000'),ts=T(sc,'spend'),ti=T(sc,'in'),cut=sc.shots[1][0]/FPS;
 if(shot===0){const dn=pr(t,tm+0.1,0.45)*(1-pr(t,cut-0.14,0.14,E.lin));
  const fo=await plate(ctx,{z:1.0,hx:880,dim:0.36*dn,focus:0.8*dn,punch:0.07});
  const st=statBlock('proof',`<div class="l1"><i></i>My best ads</div><div class="num" style="font-size:150px"></div><div class="l2">Spend</div><div class="l3">in a couple months</div>`);
  const [l1,num,l2,l3]=st.children;pop(l1,t,tm+0.02,{dy:12});
  const cp=pr(t,tnm-0.04,0.75,E.outCubic);num.innerHTML=`<span>&euro;${fmt(0*cp)}</span>`;const np=pr(t,tnm-0.06,0.3,E.outExpo);num.style.opacity=np;num.style.filter=`${GLOW_Y} blur(${((1-np)*14).toFixed(1)}px)`;num.style.transform=`scale(${mix(1.12,1,np).toFixed(4)})`;num.style.transformOrigin='0 60%';
  pop(l2,t,ts-0.04,{dy:18});pop(l3,t,ti-0.04,{dy:12});st.style.opacity=(1-pr(t,cut-0.14,0.14,E.lin)).toFixed(3);st.style.top='150px';
  shadowAt(fo.headX,fo.headY+200,dn*0.8);ctx.fx.impacts=[[tnm+0.72,0.9]];ctx.fx.orb=[tnm,0.5];
 }else{await plate(ctx,{z:1.08,hx:862,punch:0.1});ctx.fx.flashShot=0.75;}ctx.fx.vig=0.8;
};
S.pave=async ctx=>{const {t,lt,sc,sp,shot,ls,f,dur}=ctx;
 const clip=shot+1,cnt=[66,96][shot],k=Math.max(1,Math.min(cnt,1+Math.floor(ls*FPS)));
 show('pvbg');await setImg($('pvbgi'),`pvb${clip}/${pad(k,4)}.jpg`);
 show('phone');await setImg($('pvi'),`pv${clip}/${pad(k,4)}.jpg`);
 const p=pr(lt,0,0.5,E.outExpo),pc=$('phonec'),pk=1+0.05*(1-E.outExpo(ls/0.3));
 pc.style.transform=`translateX(${((1-p)*-360).toFixed(1)}px) rotateY(${(mix(38,9,p)-sp*3).toFixed(2)}deg) rotateX(${mix(6,1.5,p).toFixed(2)}deg) scale(${(mix(0.9,1,p)*pk).toFixed(4)})`;pc.style.opacity=clamp(p*1.6);
 $('pvi').style.transform=`scale(${(1.04+0.05*sp).toFixed(4)})`;
 // talking head, picture in picture
 const pip=show('pip'),pi=$('pipi');await setImg(pi,'bgs/'+pad(f+1)+'.jpg');const tk=[[1000,195],[935,205]][shot],s=0.47;
 pi.style.width=(1920*s)+'px';pi.style.height=(1080*s)+'px';pi.style.left=(192-s*tk[0]).toFixed(1)+'px';pi.style.top=(Math.min(0,Math.max(384-1080*s,46-s*tk[1]))).toFixed(1)+'px';
 const pp=pr(lt,0.12,0.45,E.outExpo),up=pr(t,T(sc,'real.')-0.34,0.5,E.inOut);pip.style.opacity=pp;pip.style.transform=`translate(${((1-pp)*200).toFixed(1)}px,${((1-up)*150).toFixed(1)}px) scale(${(mix(0.9,1,pp)*mix(1.06,1,up)).toFixed(4)})`;
 show('chips');[['c1',T(sc,'real.')],['c2',T(sc,'organic.')],['c3',T(sc,'off')]].forEach(([id,at])=>{const e=$(id),q=pr(t,at-0.04,0.4,E.outExpo);e.style.opacity=q;e.style.transform=`translateX(${((1-q)*70).toFixed(1)}px)`;e.style.filter=q<0.99?`blur(${((1-q)*7).toFixed(1)}px)`:'none';});
 ctx.fx.flash=0.9;ctx.fx.flashShot=0.5;ctx.fx.dots=0.16;ctx.fx.vig=1.5;
};
S.ugc=async ctx=>{const {t,lt,sc,sp,shot}=ctx;const tu=T(sc,'UGC'),tp=T(sc,'paid'),ts=T(sc,'street'),ta=T(sc,'absolute');
 const dn=pr(t,tu-0.1,0.4)*0.6;
 const fo=await plate(ctx,shot===0?{z:1.0,hx:880,dim:0.12*dn,punch:0.09}:{z:1.08,hx:872,dim:0.12*dn,punch:0.08});
 show('cards');const c1=$('cd1'),c2=$('cd2');
 const p1=pr(t,tu-0.06,0.46,E.outExpo),p2=pr(t,ts-0.06,0.46,E.outExpo);
 c1.style.opacity=clamp(p1*1.4)*(1-0.5*p2);c1.style.transform=`translateX(${((1-p1)*-120).toFixed(1)}px) rotateY(${(mix(64,12,p1)-sp*3).toFixed(2)}deg) rotateX(${mix(8,2,p1).toFixed(2)}deg) scale(${(1-0.06*p2).toFixed(4)})`;c1.style.filter=p1<0.99?`blur(${((1-p1)*10).toFixed(1)}px)`:(p2>0?`grayscale(${p2}) brightness(${(1-0.25*p2).toFixed(3)})`:'none');
 c1.querySelector('small').style.opacity=pr(t,tp-0.05,0.3);
 c2.style.opacity=clamp(p2*1.4);c2.style.transform=`translateX(${((1-p2)*-120).toFixed(1)}px) rotateY(${(mix(64,12,p2)-sp*3).toFixed(2)}deg) rotateX(${mix(8,2,p2).toFixed(2)}deg)`;c2.style.filter=p2<0.99?`blur(${((1-p2)*10).toFixed(1)}px)`:'none';
 c2.querySelector('small').style.opacity=pr(t,ta-0.05,0.3);
 ctx.fx.flash=0.85;ctx.fx.flashShot=0.5;ctx.fx.impacts=[[tu,0.4],[ts,0.8]];ctx.fx.orb=[ts,0.5];ctx.fx.vig=0.8;
};
const FK={src:'fake/dump.jpg',w:2240,h:1280,k:1.0,L:-200,T:0};   // image size, scale and offset in plate pixels (camera is locked off, so it stays put)
S.aiview=async ctx=>{const {t,lt,sc,sp,dur}=ctx;const tf=T(sc,'fake'),ta=T(sc,'And',1),tn=T(sc,'never');   // second 'and' = "And I don't think you'd care either"
 const w1=pr(t,tf-0.04,0.62,E.inOut),w3=pr(t,ta-0.14,0.62,E.inOut),g=w1*(1-w3);
 // sit him in the grim light: a touch cooler and flatter while the fake view is up
 $('tintm').setAttribute('values',`${(1-0.05*g).toFixed(4)} 0 0 0 0 0 ${(1-0.03*g).toFixed(4)} 0 0 0 0 0 ${(1+0.01*g).toFixed(4)} 0 0 0 0 0 1 0`);
 const fo=await plate(ctx,{z:1.0,hx:mix(900,925,g),punch:0.08,fgFilter:`url(#tint) brightness(${(1.04-0.05*g).toFixed(3)}) contrast(1.04) saturate(${(1.03-0.10*g).toFixed(3)})`});
 const fk=$('fk'),im=$('fki');fk.style.display='block';await setImg(im,FK.src);
 im.style.left=FK.L+'px';im.style.top=FK.T+'px';im.style.width=(FK.w*FK.k)+'px';im.style.height=(FK.h*FK.k)+'px';
 const X=p=>mix(-60,SW+60,p),px=x=>((x-fo.tx)/fo.zz);
 fk.style.clipPath=`inset(0 ${(1920-clamp(px(X(w1)),0,1920)).toFixed(1)}px 0 ${clamp(px(X(w3)),0,1920).toFixed(1)}px)`;
 const act=[w1,w3].find(w=>w>0.001&&w<0.999);const sn=$('scan');if(act!==undefined){sn.style.display='block';sn.style.left=(X(act)-3).toFixed(1)+'px';}
 const chip=show('aichip','flex'),ce=pr(t,tf-0.12,0.35,E.outExpo),cp=ce*(1-pr(t,ta-0.1,0.2,E.lin));$('ait').textContent='Fake view';chip.style.left='44px';chip.style.top='56px';chip.style.opacity=cp;chip.style.transform=`translateY(${((1-ce)*-30).toFixed(1)}px)`;
 [...$('aid').children].forEach((d,i)=>{d.style.opacity=(0.25+0.75*clamp(Math.sin(t*9-i*1.1))).toFixed(3)});
 const rl=show('real','flex'),rp=pr(t,ta+0.22,0.35,E.outExpo);rl.style.opacity=rp;rl.style.transform=`translateY(${((1-rp)*-20).toFixed(1)}px)`;
 ctx.fx.neg=0.07;ctx.fx.rgbAt=[[tf-0.04,0.14,10],[ta-0.14,0.14,10]];ctx.fx.impacts=[[tf+0.5,0.7]];ctx.fx.vig=0.8;
};
S.rain=async ctx=>{const {t,lt,sc,sp,shot,dur}=ctx;
 const out=E.inExpo((lt-(dur-0.15))/0.15);
 if(shot===0)await plate(ctx,{z:1.0,hx:880,punch:0.07});else await plate(ctx,{z:1.0,hx:560,punch:0.12,follow:0.3,dx:-out*900,fgFilter:'brightness(1.2) contrast(1.02) saturate(1.04)'});
 ctx.fx.rgbShot=[0,0.16,16];ctx.fx.shake=shot===1?2.2:1;ctx.fx.vig=0.8;
};
S.p62=async ctx=>{const {t,lt,sc,sp}=ctx;const tf=T(sc,'fake'),t62=T(sc,'62%'),ta=T(sc,'Americans'),tu=T(sc,'unacceptable,'),te=T(sc,'even');
 const fk=pr(t,tf-0.06,0.14,E.lin)*(1-pr(t,t62-0.2,0.14,E.lin)),dn=Math.max(fk*0.9,pr(t,t62-0.1,0.3));
 const inn=(1-E.outExpo(lt/0.34))*760;
 const duo='contrast(1.22) brightness(1.06) url(#duo) drop-shadow(0 0 26px rgba(252,239,0,.45))';
 const fo=await plate(ctx,{z:1.0,hx:855,dim:0.46*dn,focus:0.9*dn,punch:0.06,dx:inn,fgFilter:fk>0.5?duo:null});
 if(fk>0.02){const sn=show('scan2');const q=clamp((t-(tf-0.06))/Math.max(0.3,(t62-0.2)-(tf-0.06)));sn.style.left=(fo.headX-330+660*q).toFixed(1)+'px';sn.style.opacity=fk.toFixed(3);
  const chip=show('aichip','flex'),ce=pr(t,tf-0.06,0.3,E.outExpo);$('ait').textContent='Fake person';chip.style.left='44px';chip.style.top='56px';chip.style.opacity=fk.toFixed(3);chip.style.transform=`translateY(${((1-ce)*-30).toFixed(1)}px)`;
  [...$('aid').children].forEach((d,i)=>{d.style.opacity=(0.25+0.75*clamp(Math.sin(t*9-i*1.1))).toFixed(3)});}
 const st=statBlock('p62',`<div class="num" style="font-size:250px;margin-top:0"></div><div class="l2" style="font-size:42px;margin-top:-2px">of Americans</div><div class="l2" style="font-size:46px;margin-top:22px"><u>Unacceptable</u></div><div class="l3">even if you admit it&rsquo;s AI</div>`);
 st.style.top='150px';st.style.opacity=1;const [num,l2,l2b,l3]=st.children;
 const cp=pr(t,t62-0.05,0.5,E.outCubic);num.innerHTML=`<span>${fmt(62*cp)}%</span>`;const np=pr(t,t62-0.07,0.3,E.outExpo);num.style.opacity=np;num.style.filter=`${GLOW_Y} blur(${((1-np)*18).toFixed(1)}px)`;num.style.transform=`scale(${mix(1.14,1,np).toFixed(4)})`;num.style.transformOrigin='0 60%';
 pop(l2,t,ta-0.04,{dy:14});pop(l2b,t,tu-0.04,{dy:18});l2b.querySelector('u').style.setProperty('--u',pr(t,tu+0.12,0.4,E.outExpo));pop(l3,t,te-0.04,{dy:12});
 shadowAt(fo.headX,fo.headY+200,dn*0.75);
 ctx.fx.flash=0.7;ctx.fx.impacts=[[t62+0.4,1.1],[tu,0.6]];ctx.fx.orb=[t62,0.55];ctx.fx.rgbAt=[[tf-0.06,0.12,12],[t62-0.2,0.12,12]];
};
S.stats=async ctx=>{const {t,lt,sc,sp,shot}=ctx;const t82=T(sc,'82%'),t45=T(sc,'45%'),tb=T(sc,'backwards.'),tm=T(sc,'Marketers');
 const dn=pr(t,tm+0.04,0.4);
 const cfg=[{z:1.08,hx:860},{z:1.0,hx:866},{z:1.1,hx:870}][shot];
 const fo=await plate(ctx,{...cfg,dim:(shot===0?0.24:0.36)*dn,focus:0.9*dn,punch:0.08});
 // header: "Marketers have it BACKWARDS" lands mirrored, then flips the right way round and stays as the chart title
 const rw=show('rows');rw.style.top='98px';rw.style.transform='none';['rlab2','row2','row3'].forEach(id=>{$(id).style.display='none'});
 const lab=$('rlab');lab.style.display='block';lab.textContent='Marketers have it';lab.style.top='0px';pop(lab,t,tm+0.02,{dy:14});
 const r=$('row1');r.style.display='block';r.style.top='48px';r.style.filter=GLOW_Y;typeLine(r,'bw','Backwards','gy',112,tb-0.05,t);
 const fl=pr(t,tb+0.24,0.3,E.inOut);r.style.transformOrigin='50% 50%';r.style.transform=`perspective(1100px) rotateY(${(180*(1-fl)).toFixed(2)}deg)`;
 show('chart');const cc=$('chartc'),ce=t82-0.08,p=pr(t,ce,0.5,E.outExpo);cc.style.opacity=clamp(p*1.5);cc.style.transform=`translateX(${((1-p)*-140).toFixed(1)}px) rotateY(${(mix(58,10,p)-sp*2).toFixed(2)}deg) rotateX(${mix(8,2,p).toFixed(2)}deg)`;cc.style.filter=p<0.99?`blur(${((1-p)*10).toFixed(1)}px)`:'none';
 const bar=(id,at,val,slot)=>{const e=$(id),q=pr(t,at,0.8,E.outCubic),sh=pr(t,at-0.12,0.3);e.style.opacity=slot?mix(0.34*pr(t,slot,0.4),1,sh):sh;e.querySelector('.bf').style.width=(val*q).toFixed(2)+'%';const bn=e.querySelector('.bn');bn.textContent=Math.round(val*q)+'%';bn.style.opacity=sh;};
 bar('b1',t82+0.12,82);bar('b2',t45-0.04,45,t82+0.7);
 shadowAt(fo.headX,fo.headY+200,dn*0.7);
 ctx.fx.neg=0.07;ctx.fx.flashShot=0.5;ctx.fx.impacts=[[tb-0.02,0.8],[t82+0.92,0.6],[t45+0.76,0.9]];ctx.fx.orb=[t45,0.5];
};
S.close=async ctx=>{const {t,lt,sc,sp,shot}=ctx;const tn=T(sc,'never'),tf=T(sc,'fake'),th=T(sc,'human');
 const dn=pr(t,tn-0.06,0.3);
 const fo=await plate(ctx,shot===0?{z:1.0,hx:830,punch:0.08}:{z:1.04*(1+0.05*pr(t,tn-0.04,0.3,E.outExpo)),hx:mix(845,878,dn),dim:0.46*dn,focus:0.9*dn,punch:0.06});
 if(shot===1){const bt=show('bt');bt.style.left='44px';bt.style.top='156px';bt.style.filter=GLOW_Y;bt.style.opacity=1;bt.style.transformOrigin='0 50%';bt.style.transform=`scale(${(1+0.03*sp).toFixed(4)})`;typeLine(bt,'cl','Never','gy',204,tn-0.04,t);
  const rw=show('rows');rw.style.top='120px';rw.style.transform='none';['rlab','rlab2','row2','row3'].forEach(id=>{$(id).style.display='none'});
  const r=$('row1');r.style.display='block';r.style.transform='none';r.style.top='252px';r.style.filter=GLOW_W;const W=typeLine(r,'cl2','Fake human','gw',92,tf-0.04,t,{sweep:false});
  const sk=show('strike'),q=pr(t,th+0.22,0.34,E.outExpo);sk.style.left='34px';sk.style.top=(120+252+38)+'px';sk.style.width=(W+24)+'px';sk.style.transform=`rotate(-3deg) scaleX(${q.toFixed(4)})`;sk.style.opacity=q>0?1:0;
  shadowAt(fo.headX,fo.headY+200,dn*0.8);ctx.fx.impacts=[[tn,1.1],[th+0.22,0.7]];ctx.fx.orb=[tn,0.6];}
 ctx.fx.flash=0.7;ctx.fx.flashShot=0.4;
};
/* ---------------- end card ---------------- */
async function endCard(ctx){const {t}=ctx;const l=t-D.vd;
 const w=show('wall');w.style.opacity=0.34;await wallFrame(l+3);
 $('wallcam').style.transform=`translateZ(${(-560+l*36).toFixed(1)}px) rotateX(4deg) rotateY(${(-7+l*2.4).toFixed(2)}deg)`;
 show('end3d');const ex=$('ex');const N=28;
 ensure(ex,'ex',()=>{let h=`<span style="transform:translateZ(-60px);color:#FCEF00;filter:blur(38px);opacity:.75">stradvert.org</span>`;
  for(let i=N-1;i>=1;i--){const k=i/(N-1),c=`rgb(${Math.round(mix(196,84,k))},${Math.round(mix(186,78,k))},0)`;h+=`<span style="transform:translateZ(${(-i*1.2).toFixed(1)}px);color:${c}">stradvert.org</span>`;}
  h+=`<span id="exr" style="color:#FCEF00;opacity:.2;filter:blur(3px);-webkit-mask-image:linear-gradient(to top,rgba(0,0,0,.9),rgba(0,0,0,0) 62%);mask-image:linear-gradient(to top,rgba(0,0,0,.9),rgba(0,0,0,0) 62%)">stradvert.org</span>`;
  h+=`<span id="exf" style="-webkit-background-clip:text;background-clip:text;color:transparent">stradvert.org</span>`;return h;});
 if(!ex._w){const f=$('exf');ex._w=f.offsetWidth;ex._h=f.offsetHeight;[...ex.children].forEach(s=>{s.style.marginLeft=(-ex._w/2)+'px';s.style.marginTop=(-ex._h/2)+'px'});$('exr').style.transform=`translateY(${(ex._h*0.74).toFixed(1)}px) scaleY(-1)`;$('endshadow').textContent='stradvert.org';}
 const p=pr(l,0.0,0.7,E.outExpo),ry=mix(-34,-12,p)+l*3,rx=mix(16,7,p);
 ex.style.transform=`translateZ(${mix(-700,0,p).toFixed(1)}px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg)`;ex.style.opacity=clamp(p*1.8);
 const sw=pr(l,0.75,0.9,E.inOut);const xf=$('exf');xf.style.backgroundImage=`linear-gradient(104deg,rgba(255,255,255,0) 44%,rgba(255,255,255,.98) 50%,rgba(255,255,255,0) 56%),linear-gradient(180deg,#fffdc8 0%,#FCEF00 36%,#efe100 68%,#c2b600 100%)`;
 xf.style.backgroundSize=`${ex._w*3.2}px 100%,100% 100%`;xf.style.backgroundRepeat='no-repeat';xf.style.backgroundPosition=`${mix(ex._w*1.1,-ex._w*2.1,sw).toFixed(1)}px 0,0 0`;
 const fl=$('endfloor');fl.style.transform='rotateX(74deg)';fl.style.opacity=p;
 const sh=$('endshadow');sh.style.transform=`translateX(-50%) rotateX(74deg) rotateZ(${(-ry*0.25).toFixed(2)}deg) scaleY(1.5)`;sh.style.opacity=0.7*p;
 const lg=$('logo'),lp=pr(l,0.3,0.5,E.outExpo);lg.style.opacity=lp;lg.style.transform=`translateY(${((1-lp)*-24).toFixed(1)}px) scale(${mix(0.92,1,lp)})`;
 const es=$('endsub'),sp2=pr(l,0.62,0.5);es.style.opacity=sp2;es.style.letterSpacing=mix(16,8,sp2).toFixed(2)+'px';
 ctx.fx.flash=0.95;ctx.fx.dots=0.26;ctx.fx.impacts=[[D.vd+0.03,1.1]];ctx.fx.orb=[D.vd+0.1,0.6];ctx.fx.streak=[D.vd+0.75,0.9];ctx.fx.vig=1.6;
}
/* ---------------- portrait canvas (outside the square) ---------------- */
function canvasUI(t){const tn=T(D.sc[0],'never'),k=clamp((t-tn)/0.55),pu=t>=tn?Math.sin(Math.PI*k):0,hy=$('hy');
 hy.style.transform=`scale(${(1+0.06*pu).toFixed(4)})`;hy.style.filter=`drop-shadow(0 0 ${(8+18*pu).toFixed(1)}px rgba(252,239,0,${(0.45+0.5*pu).toFixed(3)}))`;
 $('pfill').style.width=(100*clamp(t/(D.total/FPS))).toFixed(3)+'%';
 $('ft').style.opacity=(1-pr(t,D.vd-0.1,0.3,E.lin)).toFixed(3);}
/* ---------------- frame ---------------- */
function sceneOf(f){let i=0;D.sc.forEach((s,k)=>{if(f>=s.f0)i=k});return D.sc[i]}
window.samples=function(f){if(f>=D.nf)return (f-D.nf)<26?6:3;const sc=sceneOf(f),t=f/FPS;
 const ev=[sc.s,...sc.shots.map(s=>s[0]/FPS),...(EV[sc.key]||[])];const hot=ev.some(e=>t-e>-0.05&&t-e<0.46)||sc.e-t<0.18;return hot?6:2;};
window.render=async function(f,sub=0){
 const t=(f+sub*SH)/FPS;hideAll();canvasUI(t);
 const ctx={f,t,fx:{}};let sc=null;
 if(f>=D.nf){ctx.lt=t-D.vd;ctx.ls=ctx.lt;await endCard(ctx);}
 else{sc=sceneOf(f);ctx.sc=sc;ctx.lt=Math.max(0,t-sc.s);ctx.dur=sc.e-sc.s;ctx.sp=clamp(ctx.lt/ctx.dur);
  let si=0;sc.shots.forEach((s,k)=>{if(f>=s[0])si=k});ctx.shot=si;ctx.ls=Math.max(0,t-sc.shots[si][0]/FPS);
  await S[sc.key](ctx);captions(ctx);}
 const fx=ctx.fx,lt=ctx.lt,ls=ctx.ls;
 const sk=fx.shake||1;let sx=nz(1,t)*2.2*sk,sy=nz(2,t)*1.7*sk,rot=nz(3,t)*0.09*sk;
 (fx.impacts||[]).forEach(([ti,a])=>{const d=t-ti;if(d>=0&&d<0.5){const k=a*12*Math.exp(-d*10);sx+=k*Math.sin(d*96+1.3);sy+=k*Math.cos(d*83+0.4);}});
 let filt='';const rg=(a,b,amp,x)=>{if(x>=a&&x<b){const k=amp*(1-(x-a)/(b-a));$('fo1').setAttribute('dx',k.toFixed(1));$('fo2').setAttribute('dx',(-k).toFixed(1));filt='url(#rgb) ';}};
 if(fx.rgb)rg(fx.rgb[0],fx.rgb[1],fx.rgb[2],lt);if(fx.rgbShot)rg(fx.rgbShot[0],fx.rgbShot[1],fx.rgbShot[2],ls);
 (fx.rgbAt||[]).forEach(([at,d,amp])=>rg(at,at+d,amp,t));
 if(fx.neg&&lt<fx.neg)filt+='invert(1) grayscale(1) contrast(1.15) ';
 const cam=$('cam');cam.style.filter=filt||'none';cam.style.transform=`translate(${sx.toFixed(2)}px,${sy.toFixed(2)}px) rotate(${rot.toFixed(4)}deg) scale(1.014)`;
 let fl=0;if(fx.flash)fl=Math.max(fl,fx.flash*Math.exp(-lt*13));if(fx.flashShot&&ctx.shot>0)fl=Math.max(fl,fx.flashShot*Math.exp(-ls*14));
 const F=$('flash');F.style.background='#fff';F.style.opacity=fl.toFixed(4);
 if(fx.fadeIn&&lt<fx.fadeIn){F.style.background='#000';F.style.opacity=(1-lt/fx.fadeIn).toFixed(4);}
 const orbs=[];if(fx.orb){const [ti,a]=fx.orb;const d=t-ti;if(d>-0.1&&d<1.3){const k=a*Math.exp(-Math.max(0,d)*2.6)*clamp((d+0.1)/0.12);orbs.push([mix(-400,700,clamp(d/1.3)),-300+d*100,k]);}}
 ['o1','o2','o3'].forEach((id,i)=>{const o=$(id);if(orbs[i]){o.style.opacity=orbs[i][2].toFixed(3);o.style.transform=`translate(${orbs[i][0].toFixed(1)}px,${orbs[i][1].toFixed(1)}px)`;}else o.style.opacity=0;});
 if(fx.streak){const [ti,a]=fx.streak;const d=t-ti;const st=$('streak');if(d>0&&d<0.9){st.style.opacity=(a*Math.sin(Math.PI*d/0.9)).toFixed(3);st.style.top=(600+d*10)+'px';st.style.transform=`scaleX(${(0.3+d*1.1).toFixed(3)})`;}}
 $('dots').style.opacity=(fx.dots!==undefined?fx.dots:(sc&&sc.look==='day'?0.035:0.07));
 $('vig').style.opacity=clamp((fx.vig||1)*0.62);
};
window.ready=(async()=>{D=await (await fetch('data.json')).json();
 const g=k=>D.sc.find(s=>s.key===k);const w=(k,x,n=0)=>T(g(k),x,n);
 EV={hook:[w('hook','never'),w('hook','view')-0.3,w('hook','view')],reason:[w('reason','more')-0.36,w('reason','polished'),w('reason','prepared'),w('reason','fake')],
  proof:[w('proof','my'),w('proof','€000,000'),w('proof','€000,000')+0.45,w('proof','spend'),w('proof','in')],pave:[w('pave','real.'),w('pave','organic.'),w('pave','off')],
  ugc:[w('ugc','UGC'),w('ugc','paid'),w('ugc','street'),w('ugc','absolute')],aiview:[w('aiview','fake')-0.12,w('aiview','fake')+0.3,w('aiview','And',1)-0.14,w('aiview','And',1)+0.25],
  rain:[g('rain').e-0.2],p62:[w('p62','fake')-0.06,w('p62','fake')+0.4,w('p62','fake')+0.85,w('p62','fake')+1.3,w('p62','62%')-0.2,w('p62','62%'),w('p62','62%')+0.4,w('p62','Americans'),w('p62','unacceptable,'),w('p62','even')],
  stats:[w('stats','Marketers'),w('stats','backwards.')-0.05,w('stats','backwards.')+0.24,w('stats','82%')-0.08,w('stats','82%')+0.12,w('stats','82%')+0.55,w('stats','45%')-0.04,w('stats','45%')+0.4],close:[w('close','never'),w('close','fake'),w('close','human')+0.22]};
 for(const f of['400 60px A','500 60px AX','600 60px AX','italic 500 60px AX','700 60px AX','800 60px AX','italic 600 60px AX','italic 800 60px AX','italic 900 60px AX','italic 900 60px MI'])await document.fonts.load(f);await document.fonts.ready;})();
