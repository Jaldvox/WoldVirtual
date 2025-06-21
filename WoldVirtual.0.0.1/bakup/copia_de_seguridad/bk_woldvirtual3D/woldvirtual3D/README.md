# Wold Virtual 3D

## Descripción
Proyecto de mundo virtual 3D con backend en Python (Reflex) y frontend en React/Three.js. Permite la exploración, creación y personalización de escenas 3D interactivas.

## Cambios y Refactorización (Sesión de hoy)
- Refactorización completa de la estructura de carpetas y archivos.
- Modularización de componentes en `src/components` (UI, 3D, formularios, datos).
- Modularización de páginas en `src/pages` (inicio, about, escena 3D, etc).
- Documentación y comentarios en todos los archivos principales.
- Mejora de la legibilidad y mantenibilidad del código.
- Se mantienen todas las funciones y aspectos originales.

## Estructura principal
```
src/
  app.py                # Entrada principal de la app Reflex
  components/           # Componentes reutilizables (UI, 3D, forms, data)
  pages/                # Páginas principales de la app
  utils/                # Utilidades generales
```

## Cómo ejecutar
1. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la app:
   ```bash
   python src/app.py
   ```

## Créditos
Refactorización y organización realizada el [fecha de hoy] para mejorar la mantenibilidad y escalabilidad del proyecto.