import {readFile,writeFile,readdir,mkdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const assets=await readdir(path.join(root,'dist/assets'));
const jsName=assets.find(name=>/^index-.*\.js$/.test(name));
const cssName=assets.find(name=>/^index-.*\.css$/.test(name));
if(!jsName||!cssName)throw new Error('Run npm run build before packaging the demo.');
let html=await readFile(path.join(root,'dist/index.html'),'utf8');
let js=await readFile(path.join(root,'dist/assets',jsName),'utf8');
const css=await readFile(path.join(root,'dist/assets',cssName),'utf8');
for(const name of ['media-room.webp','courtyard.webp']){
 const bytes=await readFile(path.join(root,'public/assets',name));
 const original='"/assets/'+name+'"';
 if(!js.includes(original))throw new Error('Could not embed artwork: '+name);
 js=js.replaceAll(original,JSON.stringify('data:image/webp;base64,'+bytes.toString('base64')));
}
js=js.replaceAll('</script','<\\/script');
html=html.replace(/<script type="module"[^>]*src="[^"]+"[^>]*><\/script>/g,'').replace(/<link rel="stylesheet"[^>]*>/g,'').replace(/<link rel="icon"[^>]*>/g,'');
html=html.replace('</head>','<style>'+css+'</style></head>').replace('</body>','<script type="module">'+js+'</script></body>');
await mkdir(path.join(root,'demo'),{recursive:true});
await writeFile(path.join(root,'demo/Signal-Play.html'),html);
console.log('Created demo/Signal-Play.html with code, styles, and artwork embedded.');
