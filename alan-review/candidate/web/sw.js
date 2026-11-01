'use strict';
const CACHE = 'alan-island-fe0882f1feb43ff1';
const ASSETS = ["./", "Body.ttf", "Chinese.otf", "app-icon.png", "cover.png", "game.html", "index.apple-touch-icon.png", "index.audio.position.worklet.js", "index.audio.worklet.js", "index.html", "index.icon.png", "index.js", "index.pck", "index.png", "index.wasm", "licenses/GODOT-LICENSE.txt", "licenses/GODOT-THIRD-PARTY-NOTICES.txt", "licenses/LICENSE-Noto.txt", "licenses/LICENSE-OpenSans.txt", "manifest.webmanifest", "pip.png"];
const URLS = ASSETS.map(path => new URL(path, self.registration.scope).href);
async function tell(message) {
  for (const client of await self.clients.matchAll({includeUncontrolled:true})) client.postMessage(message);
}
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    try {
      for (let i=0; i<URLS.length; i++) {
        await tell({type:'saving',done:i,total:URLS.length});
        const response=await fetch(new Request(URLS[i],{cache:'reload'}));
        if (!response.ok) throw new Error('Incomplete offline pack');
        await cache.put(URLS[i],response);
      }
      await cache.put(new URL('_offline_complete', self.registration.scope).href,new Response(CACHE));
      await self.skipWaiting();
      await tell({type:'ready',cache:CACHE});
    } catch(error) {
      await caches.delete(CACHE);
      await tell({type:'failed'});
      throw error;
    }
  })());
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    await self.clients.claim();
    for (const name of await caches.keys()) {
      if (name.startsWith('alan-island-') && name !== CACHE) await caches.delete(name);
    }
  })());
});
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url=new URL(event.request.url);
  url.search='';
  url.hash='';
  if (!URLS.includes(url.href)) return;
  event.respondWith((async () => {
    const cache=await caches.open(CACHE);
    const response=await cache.match(url.href);
    return response || fetch(event.request);
  })());
});
