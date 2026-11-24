import {readFile, writeFile, mkdir, copyFile, readdir} from 'node:fs/promises';
import {lines} from './src/dialogue.mjs';
import {instructionLines} from './src/instructions.mjs';
const read = name => readFile(new URL(name, import.meta.url), 'utf8');
const modules = ['state','content','language','dialogue','instructions','fieldwork','art','navigation','world','main'];
const sources = await Promise.all(modules.map(name => read('./src/'+name+'.mjs')));
const assets = await readdir(new URL('./assets/',import.meta.url));
const art = Object.fromEntries(await Promise.all(assets.filter(name=>name.endsWith('.webp')).sort().map(async name=>{
  const bytes = await readFile(new URL('./assets/'+name, import.meta.url));
  return [name.slice(0,-5),'data:image/webp;base64,'+bytes.toString('base64')];
})));
for(const role of ['scout','ranger']) {
  for(const direction of ['right','left','down','up']) {
    for(let i=0;i<6;i++) {
      if(!art[role+'-v4-'+direction+'-'+i]) throw new Error('Incomplete gait atlas: '+role+' / '+direction);
    }
  }
}
const directories=['audio/','audio/instructions/'];
const voice=Object.fromEntries((await Promise.all(directories.map(async directory=>{
  const filenames=(await readdir(new URL('./'+directory,import.meta.url))).filter(name=>name.endsWith('.mp3')).sort();
  return Promise.all(filenames.map(async name=>{
    const bytes=await readFile(new URL('./'+directory+name,import.meta.url));
    return [name.slice(0,-4),'data:audio/mpeg;base64,'+bytes.toString('base64')];
  }));
}))).flat());
for(const id of Object.keys(lines)) {
  if(!voice[id]) throw new Error('Missing Kokoro clip: '+id);
}
for(const id of Object.keys(instructionLines)) {
  if(!voice[id]) throw new Error('Missing instruction clip: '+id);
}
const game = 'const ART = '+JSON.stringify(art)+';\nconst VOICE = '+JSON.stringify(voice)+';\n'+sources.map(source => source.replace(/^import .*;\n/gm,'').replace(/^export /gm,'')).join('\n');
const phaser = await read('./node_modules/phaser/dist/phaser.min.js');
const css = (await read('./src/style.css'))+'\n'+(await read('./src/fieldwork.css'));
const page = await read('./index.html');
const script = content => '<script>'+content.replace(/<\/script/gi,'<\\/script')+'</script>';
const output = page.replace('<!-- CSS -->',()=>'<style>'+css+'</style>')
  .replace('<!-- SCRIPTS -->',()=>script(phaser)+script('(()=>{\n'+game+'\n})();'));
await mkdir(new URL('./build/',import.meta.url),{recursive:true});
await writeFile(new URL('./build/Broken-Bridge-v0.5.0.html',import.meta.url),output);
await copyFile(new URL('./node_modules/phaser/LICENSE.md',import.meta.url),new URL('./build/PHASER-LICENSE.txt',import.meta.url));
await copyFile(new URL('./OFFLINE-README.txt',import.meta.url),new URL('./build/OFFLINE-README.txt',import.meta.url));
