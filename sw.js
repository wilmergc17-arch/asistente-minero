const CACHE = "asistente-minero-0.2.0";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png"];
const EXTRA = [
  "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap",
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(async c => {
  await c.addAll(SHELL);
  await Promise.all(EXTRA.map(u => fetch(u, {mode: "no-cors"}).then(r => c.put(u, r)).catch(() => {})));
}).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, {ignoreSearch: e.request.mode === "navigate"}).then(hit => hit || fetch(e.request).then(r => {
    if (r && (r.ok || r.type === "opaque")) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); }
    return r;
  }).catch(() => e.request.mode === "navigate" ? caches.match("index.html") : undefined)));
});
