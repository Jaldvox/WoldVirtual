# Complemento React/Three.js para World Virtual

Este complemento será el visor 3D avanzado del metaverso, construido con React y Three.js, e integrado con Reflex.

## Objetivo
- Renderizar escenas 3D interactivas usando Three.js.
- Recibir estado y props desde Reflex (backend Python).
- Emitir eventos (clics, movimientos) hacia Reflex para lógica de juego y sincronización.

## Estructura sugerida
- `src/ThreeCanvas.jsx`: Componente base para la escena 3D (placeholder inicial).
- `src/components/`: Carpeta para futuros componentes 3D.
- `src/assets/`: Modelos, imágenes, recursos.

## Primeros pasos
1. Instala dependencias: `npm install`
2. Lanza el entorno: `npm run dev`
3. Empieza a desarrollar en `src/ThreeCanvas.jsx` y conecta con Reflex según la documentación. 