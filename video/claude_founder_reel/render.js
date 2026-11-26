const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const frames=process.argv[2]?process.argv[2].split(',').map(Number):[...Array(1018).keys()];const outdir=process.argv[3]||'out';const N=+process.argv[4]||4;
const srv=http.createServer((q,r)=>{const p=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return}r.end(d)})}).listen(0,async()=>{
 const port=srv.address().port;const b=await chromium.launch();
 await Promise.all([...Array(N).keys()].map(async w=>{const pg=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});await pg.goto(`http://localhost:${port}/comp.html`);await pg.evaluate(()=>window.ready);
  for(let i=w;i<frames.length;i+=N){const f=frames[i];await pg.evaluate(f=>window.render(f),f);await pg.screenshot({path:`${outdir}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:97});}
 }));await b.close();srv.close();});
