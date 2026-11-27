// usage: node render3.js still 10,20,30 outdir   |   node render3.js full  start end workers
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const mode=process.argv[2];
const srv=http.createServer((q,r)=>{const p=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return}
  const ext=path.extname(p);r.writeHead(200,{'Content-Type':{'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'}[ext]||'application/octet-stream','Cache-Control':'max-age=3600'});r.end(d)})}).listen(0,async()=>{
 const port=srv.address().port;const b=await chromium.launch({args:['--disable-web-security','--force-color-profile=srgb']});
 async function mk(){const pg=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});pg.on('console',m=>{const t=m.text();if(t.startsWith('IMGERR')||m.type()==='error')console.log('[page]',t)});pg.on('pageerror',e=>console.log('[pageerror]',e.message));
  await pg.goto(`http://localhost:${port}/comp.html`);await pg.evaluate(()=>window.ready);return pg}
 if(mode==='still'){const frames=process.argv[3].split(',').map(Number);const out=process.argv[4]||'test';fs.mkdirSync(out,{recursive:true});const N=4;
  await Promise.all([...Array(N).keys()].map(async w=>{const pg=await mk();for(let i=w;i<frames.length;i+=N){const f=frames[i];const t0=Date.now();await pg.evaluate(f=>window.render(f,0),f);await pg.screenshot({path:`${out}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});if(process.env.TIME)console.log(f,Date.now()-t0,'ms')}}));
 }else{const s=+process.argv[3],e=+process.argv[4],N=+process.argv[5]||4;fs.mkdirSync('sub',{recursive:true});let done=0,shots=0;const t0=Date.now();
  await Promise.all([...Array(N).keys()].map(async w=>{const pg=await mk();for(let f=s+w;f<e;f+=N){const n=await pg.evaluate(f=>window.samples(f),f);
    for(let i=0;i<n;i++){await pg.evaluate(([f,sub])=>window.render(f,sub),[f,i/n]);await pg.screenshot({path:`sub/${String(f).padStart(5,'0')}_${i}.jpg`,type:'jpeg',quality:95});shots++}
    fs.writeFileSync(`sub/${String(f).padStart(5,'0')}.n`,String(n));done++;if(done%60===0)console.log('frames',done,'shots',shots,((Date.now()-t0)/1000).toFixed(0)+'s')}}));
  console.log('RENDER_DONE frames',done,'shots',shots,((Date.now()-t0)/1000).toFixed(0)+'s');}
 await b.close();srv.close();});
