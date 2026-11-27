// Renders the storyboard phone from the concept page (only the phone element, nothing that names the brand) to sb/%05d.jpg
// usage: node sb.js <page.html> <frames> ; three beats, hard-driven so every frame is deterministic
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const src=process.argv[2],N=+process.argv[3]||92;const BEATS=[[0,1.55],[1.55,3.4]],SHOW=[0,2],XF=0.14;   // two of the five storyboard frames: the question, then the follow-up
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1100,height:1500},deviceScaleFactor:3});
 await pg.addInitScript(()=>{window.setTimeout=()=>0;});
 await pg.goto('file://'+path.resolve(src));await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(800);
 fs.mkdirSync('sb',{recursive:true});
 const box=await pg.evaluate(()=>{const p=document.querySelector('.phone');p.scrollIntoView({block:'center'});const r=p.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}});
 const fonts=await pg.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight));console.log('fonts loaded:',[...new Set(fonts)].join(', '));
 for(let i=0;i<N;i++){const t=i/30;
  await pg.evaluate(([t,BEATS,XF,SHOW])=>{const fr=[...document.querySelectorAll('.frame')],sg=[...document.querySelectorAll('.seg')];let st=0;BEATS.forEach((b,j)=>{if(t>=b[0])st=j});const k=SHOW[st],kp=st>0?SHOW[st-1]:-1;
   fr.forEach((f,j)=>{f.style.transition='none';let o=j===k?1:0;if(j===kp){o=Math.max(0,1-(t-BEATS[st][0])/XF)}f.style.opacity=o;f.style.zIndex=j===k?2:1;});
   sg.forEach((s,j)=>{s.className='seg';const bar=s.firstChild;bar.style.animation='none';bar.style.width=(j<k?100:j===k?Math.min(100,100*(t-BEATS[st][0])/(BEATS[st][1]-BEATS[st][0])):0)+'%';});},[t,BEATS,XF,SHOW]);
  await pg.screenshot({path:`sb/${String(i+1).padStart(5,'0')}.jpg`,type:'jpeg',quality:95,clip:box});}
 console.log('storyboard frames',N,'box',JSON.stringify(box));await b.close();})();
