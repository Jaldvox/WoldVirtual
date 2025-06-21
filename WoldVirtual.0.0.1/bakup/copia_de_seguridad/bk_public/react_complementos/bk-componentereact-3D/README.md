# bk-componentereact-3D

## Descripción
Este directorio contiene el componente React que servirá como interfaz de usuario (UI) para el metaverso, integrándose con el entorno 3D desarrollado en la carpeta `webgl threejs`.

---

## Estado actual de la integración
- El entorno 3D ya está funcional y preparado para integración:
  - Incluye suelo, cubo, esfera y cilindro de prueba.
  - El cubo está animado (rotación automática).
  - Detección de clics en cubo, esfera y cilindro (nombre en consola).
  - Ejes de referencia (AxesHelper) para orientación.
  - Resaltado de objetos al pasar el ratón (hover).
  - Tooltip contextual con el nombre del objeto bajo el cursor.

---

## Sugerencias para la integración React ↔️ Three.js
- Puedes aprovechar la detección de clics y el hover para disparar eventos en React (por ejemplo, mostrar información contextual, abrir paneles de UI o resaltar elementos en la interfaz).
- Mantén la UI React desacoplada del motor 3D. Usa eventos personalizados, props o contextos para la comunicación.
- Utiliza refs o IDs para acceder al canvas 3D desde React si necesitas interacción directa.

---

## Puntos pendientes y próximos pasos
- Implementar carga de modelos GLTF/GLB desde archivos o URLs.
- Documentar y exponer una API de eventos para que React pueda comunicarse con el entorno 3D (por ejemplo, mover objetos, recibir notificaciones de interacción, etc.).
- Mejorar la interacción visual (más efectos, tooltips avanzados, etc.).
- Preparar la integración con Reflex (backend Python) para la lógica central y conexión blockchain.

---

## Estructura recomendada
```
bk-componentereact-3D/
│
├── src/
│   ├── components/         # Componentes UI (paneles, menús, inventario, chat, etc.)
│   ├── hooks/              # Hooks personalizados para lógica/metaverso
│   ├── utils/              # Utilidades compartidas
│   ├── App.jsx             # Punto de entrada principal
│   └── index.js            # Renderizado ReactDOM
├── public/
│   └── index.html          # HTML base
├── package.json            # Dependencias y scripts
└── README.md               # Esta documentación
```

---

## Notas finales
- Consulta este README y el de `webgl threejs` antes de avanzar a la integración avanzada.
- Documenta bien cada componente y su propósito para facilitar el trabajo en equipo. 