# threejs3D

## Descripción
Módulo de utilidades y ejemplos para la integración de Three.js en el proyecto Wold Virtual 3D.

## Cambios y Refactorización (Sesión de hoy)
- Modularización de scripts: `scene.js`, `camera.js`, `renderer.js`, `objects/cube.js`.
- Integración con la estructura general del backend y frontend.
- Mejor documentación y comentarios en los archivos principales.
- Mantiene la funcionalidad original, pero con mejor organización.

## Estructura principal
```
src/
  main.js        # Inicialización de la escena 3D
  scene.js       # Configuración de la escena
  camera.js      # Configuración de la cámara
  renderer.js    # Configuración del renderer
  objects/       # Objetos 3D reutilizables
```

## Cómo usar
Importa los módulos desde `src/` en tu frontend o backend según sea necesario.

## Créditos
Refactorización y organización realizada el [fecha de hoy] para mejorar la integración y mantenibilidad.