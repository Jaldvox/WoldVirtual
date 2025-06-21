# Three.js Components

Esta carpeta contiene los componentes principales para la escena 3D:

- **ThreeCanvas.jsx**: Componente raíz/canvas que inicializa la escena, cámara y renderizador Three.js. Recibe entidades y callbacks para eventos.
- **EntityCube.jsx**: Componente de entidad básica (cubo/avatar) que acepta props de posición, rotación, escala y expone eventos (ej. clic).
- **Integración**: Estos componentes están preparados para recibir estado desde Reflex y reportar eventos usando el servicio `ReflexConnection` (WebSocket).

Esta estructura permite la comunicación bidireccional y la modularidad para futuras extensiones (más entidades, controles, etc.). 