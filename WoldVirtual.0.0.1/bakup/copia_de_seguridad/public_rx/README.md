# Plantilla Modular Reflex: World Virtual

Esta carpeta contiene la base modularizada para la app principal del metaverso World Virtual usando Reflex.

## Estructura
- `state.py`: Estado global, usuario, red, métodos de ejemplo.
- `header.py`: Header superior con menú de redes y navegación.
- `main_content.py`: Zona principal de contenido.
- `threejs_viewer.py`: Placeholder para la futura integración 3D.
- `index.py`: Punto de entrada que compone la app y configura el tema.

## Extensión
- Añade módulos según crezca la lógica (blockchain, storage, endpoints REST, etc).
- Documenta cada función y clase para facilitar la colaboración.
- Integra el visor 3D en `threejs_viewer.py` cuando esté listo el frontend React/Three.js. 