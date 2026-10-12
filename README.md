# Asistente Minero

App para Android (PWA) de consulta minera con enfoque en minería subterránea peruana y SSOMA. Funciona sin conexión después de abrirla una vez.

**Abrir e instalar:** https://wilmergc17-arch.github.io/asistente-minero/
En Chrome para Android: menú ⋮ → "Instalar app" o "Agregar a pantalla principal".

## Contenido
- **Preguntar a la IA (con internet):** gratis, prepara la pregunta con la base y la abre en Claude, ChatGPT, Gemini, Copilot, Perplexity o DeepSeek; opcionalmente, con clave de API de pago, chat directo con Claude que usa la base de la app, tus documentos y búsqueda web; ayuda a decidir; lee fotos y PDF con “Leer con IA” y guarda lo aprendido para usarlo sin conexión. Usa tu propia clave de API de Anthropic, guardada solo en el teléfono.
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
