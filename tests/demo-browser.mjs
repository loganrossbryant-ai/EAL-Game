import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';

// Serve the exact downloadable bytes, with no Vite transforms or asset fallback.
const html=await readFile(new URL('../demo/Signal-Play.html',import.meta.url));
const unexpected=[];
const server=createServer((req,res)=>{
 if(req.url==='/favicon.ico'){res.writeHead(204);res.end();return;}
 if(req.url!=='/'){unexpected.push(req.url);res.writeHead(404);res.end();return;}
 res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(html);
});
await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
const previousURL=process.env.BASE_URL;
const previousScreenshots=process.env.SCREENSHOT_DIR;
process.env.BASE_URL=`http://127.0.0.1:${server.address().port}`;
process.env.SCREENSHOT_DIR='test-results/demo';
try{
 await import('./browser.mjs');
 assert.deepEqual(unexpected,[],'The downloaded game must not depend on external asset files.');
 console.log('PASS: exact downloadable HTML completed the full browser journey without separate asset requests.');
}finally{
 if(previousURL===undefined)delete process.env.BASE_URL;else process.env.BASE_URL=previousURL;
 if(previousScreenshots===undefined)delete process.env.SCREENSHOT_DIR;else process.env.SCREENSHOT_DIR=previousScreenshots;
 await new Promise(resolve=>server.close(resolve));
}
