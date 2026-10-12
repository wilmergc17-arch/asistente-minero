import json, sys, os
S, KBP, OUT, ART = sys.argv[1:5]
kb = json.load(open(KBP, encoding="utf-8"))
kbs = json.dumps(kb, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
tpl = open(os.path.join(S, "app_template.html"), encoding="utf-8").read().replace("__KB__", kbs)
open(ART, "w", encoding="utf-8").write(tpl)
head, body = tpl.split('<div class="app">', 1)
os.makedirs(OUT, exist_ok=True)
html = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + '</head>\n<body>\n<div class="app">' + body + '</body>\n</html>\n')
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
manifest = {"name": "Asistente Minero", "short_name": "Asist. Minero", "lang": "es-PE",
  "description": "Asistente de minería subterránea peruana con SSOMA, glosario, procesos, logística, CAPEX y OPEX. Funciona sin conexión.",
  "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait",
  "background_color": "#1d2a2c", "theme_color": "#1d2a2c",
  "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
json.dump(manifest, open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ver = kb["version"]
sw = """const CACHE = "asistente-minero-%s";
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
""" % ver
open(os.path.join(OUT, "sw.js"), "w").write(sw)
from PIL import Image, ImageDraw
for n in (192, 512):
    im = Image.new("RGB", (n, n), (29, 42, 44)); d = ImageDraw.Draw(im); u = n / 16
    d.pieslice([3*u, 4*u, 13*u, 14*u], 180, 360, fill=(224, 179, 71))   # casco
    d.rectangle([2*u, 8.6*u, 14*u, 10*u], fill=(224, 179, 71))          # ala
    d.ellipse([6.9*u, 5.2*u, 9.1*u, 7.4*u], fill=(241, 239, 230))        # lámpara
    d.polygon([(4*u, 13*u), (8*u, 11*u), (12*u, 13*u)], fill=(194, 65, 12))  # roca
    im.save(os.path.join(OUT, f"icon-{n}.png"))
print("ok", len(html))
