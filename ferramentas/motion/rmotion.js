// uso: node rmotion.js pagina.html saida.mp4 [fps]
const {chromium}=require('playwright');const {execSync}=require('child_process');const fs=require('fs'),path=require('path');
(async()=>{const [pg,out,fpsA]=process.argv.slice(2);const fps=+(fpsA||30);const dir=path.join(path.dirname(out),'frames');fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.resolve(pg));await p.waitForTimeout(800);
const D=await p.evaluate(()=>window.DUR);const N=Math.round(D*fps);
for(let i=0;i<N;i++){await p.evaluate(t=>window.render(t),i/fps);await p.screenshot({path:path.join(dir,String(i).padStart(5,'0')+'.jpg'),type:'jpeg',quality:95});}
await b.close();execSync(`ffmpeg -v error -y -framerate ${fps} -i ${dir}/%05d.jpg -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart ${out}`);console.log('ok',N,'frames');})();
