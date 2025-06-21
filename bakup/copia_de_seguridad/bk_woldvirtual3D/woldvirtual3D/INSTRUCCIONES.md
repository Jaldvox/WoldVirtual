# Instrucciones para Wold Virtual 3D

## ✅ Problemas Resueltos

### 1. Configuración de Reflex
- ✅ Creado `rxconfig.py` con configuración correcta
- ✅ Deshabilitado Tailwind CSS para evitar warnings
- ✅ Configurado para desarrollo y producción

### 2. Estructura de Archivos
- ✅ Refactorización completa de componentes y páginas
- ✅ Documentación mejorada en todos los archivos
- ✅ Estructura modular organizada

### 3. Frontend Three.js
- ✅ Archivos JavaScript organizados y documentados
- ✅ Interfaz de usuario funcional
- ✅ Controles interactivos para la escena 3D

## 🚀 Cómo Ejecutar la Aplicación

### Opción 1: Backend Reflex (Recomendado)
```bash
# Desde el directorio woldvirtual3D
python src/app.py
```

### Opción 2: Frontend Directo
```bash
# Abrir public/index.html en el navegador
# O usar un servidor local:
python -m http.server 8000
# Luego ir a http://localhost:8000/public/
```

### Opción 3: React App
```bash
cd complemento3d-app
npm install
npm start
```

## 🔧 Solución de Problemas

### Carpeta Duplicada
Si encuentras el error de carpeta duplicada `public/public`:

1. **Ejecutar script de limpieza:**
   ```bash
   cleanup.bat
   ```

2. **Manual (si el script no funciona):**
   - Cerrar todas las aplicaciones que puedan estar usando los archivos
   - Reiniciar el explorador de archivos
   - Eliminar manualmente la carpeta `public/public`

### Dependencias
Si hay problemas con las dependencias:
```bash
pip install -r requirements.txt
```

### Puerto en Uso
Si el puerto 8000 está ocupado:
- Cambiar el puerto en `src/app.py`
- O matar el proceso que use el puerto

## 📁 Estructura del Proyecto

```
woldvirtual3D/
├── src/                    # Backend Reflex
│   ├── app.py             # Aplicación principal
│   ├── components/        # Componentes reutilizables
│   └── pages/            # Páginas de la aplicación
├── public/               # Frontend estático
│   ├── index.html        # Página principal
│   ├── assets/           # CSS y recursos
│   └── js/              # JavaScript
├── complemento3d-app/    # Aplicación React
├── threejs3D/           # Módulos Three.js
├── rxconfig.py          # Configuración Reflex
├── requirements.txt     # Dependencias Python
└── README.md           # Documentación
```

## 🎮 Funcionalidades

### Escena 3D
- ✅ Rotación de objetos
- ✅ Controles de cámara (zoom, pan, rotate)
- ✅ Agregar objetos (cubo, esfera, plano)
- ✅ Control de luces
- ✅ Configuración de FOV y velocidad

### Interfaz
- ✅ Controles en tiempo real
- ✅ Información de la escena (FPS, objetos, memoria)
- ✅ Screenshots
- ✅ Modo VR (en desarrollo)

## 📝 Notas Importantes

1. **Reflex**: La aplicación principal usa Reflex para el backend
2. **Three.js**: Renderizado 3D en el navegador
3. **Modular**: Código organizado en módulos reutilizables
4. **Responsive**: Interfaz adaptada para diferentes dispositivos

## 🆘 Soporte

Si encuentras problemas:
1. Revisar la consola del navegador para errores JavaScript
2. Verificar que todas las dependencias estén instaladas
3. Comprobar que los puertos no estén ocupados
4. Ejecutar el script de limpieza si hay problemas de archivos

---

**Refactorización completada el 21/06/2025**
*Manteniendo todas las funciones originales con mejor organización y documentación* 