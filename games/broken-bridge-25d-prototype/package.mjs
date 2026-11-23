import {readFile, writeFile, mkdir, copyFile} from 'node:fs/promises';
const read = name => readFile(new URL(name, import.meta.url), 'utf8');
const modules = ['state','content','art','world','main'];
const sources = await Promise.all(modules.map(name => read('./src/'+name+'.mjs')));
const game = sources.map(source => source.replace(/^import .*;\n/gm,'').replace(/^export /gm,'')).join('\n');
const phaser = await read('./node_modules/phaser/dist/phaser.min.js');
const css = await read('./src/style.css');
const page = await read('./index.html');
const script = content => '<script>'+content.replace(/<\/script/gi,'<\\/script')+'</script>';
const output = page.replace('<!-- CSS -->',()=>'<style>'+css+'</style>')
  .replace('<!-- SCRIPTS -->',()=>script(phaser)+script('(()=>{\n'+game+'\n})();'));
await mkdir(new URL('./build/',import.meta.url),{recursive:true});
await writeFile(new URL('./build/Broken-Bridge-v0.1.0.html',import.meta.url),output);
await copyFile(new URL('./node_modules/phaser/LICENSE.md',import.meta.url),new URL('./build/PHASER-LICENSE.txt',import.meta.url));
await copyFile(new URL('./OFFLINE-README.txt',import.meta.url),new URL('./build/OFFLINE-README.txt',import.meta.url));
