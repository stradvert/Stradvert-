const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const srv=http.createServer((q,r)=>{const p=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return}r.writeHead(200);r.end(d)})}).listen(0,async()=>{
 const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1080}});await pg.goto(`http://localhost:${srv.address().port}/comp.html`);await pg.evaluate(()=>window.ready);
 const res=await pg.evaluate(()=>{const out={};const m=(txt,css)=>{const s=document.createElement('span');s.style.cssText='position:absolute;white-space:nowrap;visibility:hidden;'+css;s.textContent=txt;document.body.appendChild(s);const w=s.offsetWidth;s.remove();return w};
  const A='font-family:A;text-transform:uppercase;letter-spacing:3px;font-kerning:none;line-height:1;';
  [['Never',236],['Never',200],['Fake human',114],['Fake human',92],['62%',300],['62%',250],['Polished',116],['Prepared',116],['Fake',256],['Backwards',112],['Backwards',120]].forEach(([t,s])=>out[t+'@'+s]=m(t,A+'font-size:'+s+'px'));
  out['num107@158']=m('€107,000','font-family:A;letter-spacing:2px;font-size:158px');out['num107@150']=m('€107,000','font-family:A;letter-spacing:2px;font-size:150px');
  out['unacc54']=m('Unacceptable','font:italic 800 54px/1 AX;font-stretch:125%;text-transform:uppercase;letter-spacing:.5px');
  out['unacc46']=m('Unacceptable','font:italic 800 46px/1 AX;font-stretch:125%;text-transform:uppercase;letter-spacing:.5px');
  out['ofam44']=m('of Americans','font:italic 800 44px/1 AX;font-stretch:125%;text-transform:uppercase;letter-spacing:.5px');
  out['url124']=m('stradvert.org','font:italic 900 124px/1 AX;font-stretch:125%;letter-spacing:-2.5px');
  out['url104']=m('stradvert.org','font:italic 900 104px/1 AX;font-stretch:125%;letter-spacing:-2.5px');
  // captions: full width of every group
  const cap=document.getElementById('cap');cap.style.display='block';const rows=[];
  for(const c of D.caps){const sc=D.sc.find(s=>s.key===c.sc);cap.innerHTML=sc.w.slice(c.a,c.b).map(w=>`<span class="w ${w[2]?'k':''}">${w[0]}</span>`).join('');
   const kids=[...cap.children];cap.style.whiteSpace='nowrap';const wd=cap.scrollWidth;cap.style.whiteSpace='';rows.push([c.sc,kids.map(k=>k.textContent).join(' '),wd>968?2:1,Math.round(wd)]);}
  out.caps=rows;return out});
 for(const k in res){if(k!=='caps')console.log(k,res[k])}res.caps.forEach(r=>console.log((r[2]>1?'WRAP ':'     ')+r[3]+'px  '+r[0]+': '+r[1]));
 await b.close();srv.close();});
