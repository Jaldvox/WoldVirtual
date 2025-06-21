# Carpeta Assets

## Descripción
Esta carpeta contiene todos los recursos estáticos necesarios para el metaverso, incluyendo modelos 3D, texturas, sonidos y otros archivos multimedia.

## Estructura de Carpetas

### `/models`
- Modelos 3D en formato glTF/GLB
- Avatares
- Objetos
- Terrenos
- Edificios

### `/textures`
- Texturas PBR
- Mapas de normales
- Mapas de rugosidad
- Mapas de metalicidad
- Mapas de oclusión

### `/sounds`
- Efectos de sonido
- Música ambiental
- Sonidos de interacción
- Audio espacial

### `/images`
- Iconos
- UI elements
- Thumbnails
- Sprites

## Formatos Soportados

### Modelos 3D
- glTF/GLB (preferido)
- FBX
- OBJ
- STL

### Texturas
- PNG
- JPG
- HDR
- EXR

### Audio
- MP3
- WAV
- OGG

## Convenciones de Nombrado
- Usar snake_case para nombres de archivos
- Incluir resolución en nombres de texturas (ej: `wall_2k.png`)
- Incluir LOD en nombres de modelos (ej: `tree_lod0.glb`)
- Usar prefijos descriptivos (ej: `tex_`, `mod_`, `snd_`)

## Optimización
- Comprimir texturas
- Optimizar modelos 3D
- Usar LOD para modelos complejos
- Implementar streaming de assets

## Uso
```python
from assets import load_model, load_texture, load_sound

# Cargar un modelo
model = load_model("models/avatar.glb")

# Cargar una textura
texture = load_texture("textures/wall_2k.png")

# Cargar un sonido
sound = load_sound("sounds/ambient.mp3")
```

## 🐛 Reportar Problemas

Si encuentras algún problema con los assets o tienes sugerencias para mejorar, por favor:

1. Verifica si el problema ya ha sido reportado en la [sección de issues](https://github.com/tu-usuario/woldvirtual/issues)
2. Si no existe, crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Capturas de pantalla si aplica
   - Información del sistema

## 🤝 Contribución

Para contribuir con nuevos assets:

1. Asegúrate de seguir las convenciones de nombrado
2. Optimiza los archivos antes de subirlos
3. Incluye metadatos relevantes
4. Verifica los derechos de uso
5. Crea un pull request con una descripción detallada

## 📝 Licencia

Los assets están bajo la Licencia MIT. Ver [LICENSE.md](../LICENSE.md) para más detalles. 