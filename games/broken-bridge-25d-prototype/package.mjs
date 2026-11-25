import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir, copyFile, readdir} from 'node:fs/promises';
import {lines} from './src/dialogue.mjs';
import {instructionLines} from './src/instructions.mjs';
import {fieldLines} from './src/field-dialogue.mjs';

const path = name => new URL(name, import.meta.url);
const read = name => readFile(path(name), 'utf8');
const dataUrl=(bytes,type)=>'data:'+type+';base64,'+bytes.toString('base64');
const {version}=JSON.parse(await read('./package.json'));
const modules=['survey','state','content','language','dialogue','instructions','field-dialogue',
  'field-stations','fieldwork','river','art','navigation','world','soundscape','main'];
const sources=await Promise.all(modules.map(name=>read('./src/'+name+'.mjs')));
const assets=await readdir(path('./assets/'));
// The archived moving strips stay with their original release source.
const retiredStreams=new Set(['stream-amber.webp','stream-jade.webp','stream-wake.webp']);
const art=Object.fromEntries(await Promise.all(assets.filter(name=>name.endsWith('.webp')&&!retiredStreams.has(name)).sort().map(async name=>{
  const bytes=await readFile(path('./assets/'+name));
  return [name.slice(0,-5),dataUrl(bytes,'image/webp')];
})));
for(const role of ['scout','ranger']){
  for(const direction of ['right','left','down','up']){
    for(let i=0;i<6;i++){
      if(!art[role+'-v4-'+direction+'-'+i])throw new Error('Incomplete gait atlas: '+role+' / '+direction);
    }
  }
}
for(const name of ['wind-fern','wind-reed','wind-fir','wind-cedar','survey-winch','bridge-rig',
  'survey-water','trail-overview','ridge-mist','scenery-bank']){
  if(!art[name])throw new Error('Missing field art: '+name);
}

async function loadBank(directory,type,captions){
  const {clips}=JSON.parse(await read(directory+'manifest.json'));
  if(captions&&Object.keys(clips).length!==Object.keys(captions).length){
    throw new Error('Incorrect voice bank size: '+directory);
  }
  return Promise.all(Object.keys(clips).sort().map(async id=>{
    const {file,sha256,caption}=clips[id];
    if(captions&&(!Object.hasOwn(captions,id)||captions[id]!==caption))throw new Error('Incorrect caption: '+id);
    const bytes=await readFile(path(directory+file));
    if(createHash('sha256').update(bytes).digest('hex')!==sha256)throw new Error('Incorrect audio checksum: '+id);
    return [id,dataUrl(bytes,type)];
  }));
}
const voiceEntries=(await Promise.all([
  loadBank('./audio/','audio/mpeg',lines),
  loadBank('./audio/instructions/','audio/mpeg',instructionLines),
  loadBank('./audio/field-dialogue/','audio/mpeg',fieldLines),
])).flat();
const voices=Object.fromEntries(voiceEntries);
if(Object.keys(voices).length!==voiceEntries.length)throw new Error('Duplicate voice line IDs');
const soundEntries=(await Promise.all([
  loadBank('./audio/world/','audio/wav'),
  loadBank('./audio/music/','audio/wav'),
])).flat();
const soundBank=Object.fromEntries(soundEntries);
if(Object.keys(soundBank).length!==soundEntries.length||!soundBank['clearing-music']){
  throw new Error('Invalid world sound or music bank');
}

const game='const ART='+JSON.stringify(art)+';\nconst VOICE='+JSON.stringify(voices)+
  ';\nconst WORLD_AUDIO='+JSON.stringify(soundBank)+';\n'+
  sources.map(source=>source.replace(/^import .*;\n/gm,'').replace(/^export /gm,'')).join('\n');
const phaser=await read('./node_modules/phaser/dist/phaser.min.js');
const css=(await Promise.all(['style','fieldwork','stations'].map(name=>read('./src/'+name+'.css')))).join('\n');
const page=await read('./index.html');
const script=content=>'<script>'+content.replace(/<\/script/gi,'<\\/script')+'</script>';
const output=page.replace('<!-- CSS -->',()=>'<style>'+css+'</style>')
  .replace('<!-- SCRIPTS -->',()=>script(phaser)+script('(()=>{\n'+game+'\n})();'));
await mkdir(path('./build/'),{recursive:true});
await writeFile(path('./build/Broken-Bridge-v'+version+'.html'),output);
await copyFile(path('./node_modules/phaser/LICENSE.md'),path('./build/PHASER-LICENSE.txt'));
await copyFile(path('./OFFLINE-README.txt'),path('./build/OFFLINE-README.txt'));
