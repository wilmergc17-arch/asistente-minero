# Asistente Minero

App para Android (PWA) de consulta minera con enfoque en minería subterránea peruana y SSOMA. Funciona sin conexión después de abrirla una vez.

**Abrir e instalar:** https://wilmergc17-arch.github.io/asistente-minero/
En Chrome para Android: menú ⋮ → "Instalar app" o "Agregar a pantalla principal".

## Contenido
- **Preguntar a la IA (con internet):** responde dentro de la app con Gemini de Google (clave gratuita de AI Studio) o Claude (clave de pago). Usa la base de la app y tus documentos; lee fotos y PDF con “Leer con IA” y guarda lo aprendido para usarlo sin conexión. Las claves se guardan solo en el teléfono.
- Seguridad y SSOMA (D.S. 024-2016-EM, Ley 29783), glosario peruano, procesos, logística, CAPEX/OPEX, preguntas frecuentes y empresa de referencia (Consorcio Minero Horizonte).
- 9 calculadoras: factor de acoplamiento, punto de reorden, IF/IS/IA, caudal de aire, costo por metro, ley diluida, ley de corte, VAN y costo horario.
- Mis documentos: PDF, textos y fotos guardados en el teléfono e incluidos en el buscador.

## Cómo regenerar
```
python3 fuente/build_kb.py fuente            # base v0.1
python3 fuente/peru_patch.py fuente          # adapta a Perú + SSOMA (v0.2)
python3 fuente/build_app.py fuente fuente/base_conocimiento.json . /tmp/preview.html
```
Al cambiar la base, sube la versión en `base_conocimiento.json` para que el teléfono descargue la actualización.

Los valores normativos y de costos son referenciales: verifica siempre la norma vigente y los estándares de tu unidad.

## App Android (APK)

El workflow `APK Android` empaqueta la app web dentro de un WebView (carpeta `android/`) y publica
`asistente-minero.apk` en Releases: https://github.com/wilmergc17-arch/asistente-minero/releases/latest/download/asistente-minero.apk

Para firmar siempre con la misma llave (y actualizar sin desinstalar) agrega los secretos
`ANDROID_KEYSTORE_B64` y `ANDROID_KS_PASS` en Settings > Secrets and variables > Actions.
