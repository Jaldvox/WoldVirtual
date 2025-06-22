# 📁 Estructura del Proyecto Wold Virtual

## 🎯 Visión General

Este documento explica la estructura organizacional del proyecto Wold Virtual después de la reorganización realizada en junio de 2025.




### **🎯 ¿Cómo Contribuir?**

Tu participación es fundamental para el éxito de 
**WoldVirtual Crypto 3D**. Ofrecemos múltiples 
formas de contribución para desarrolladores de 
todos los niveles.

<div align="center">

### **📋 Portal de Contribuciones**

[![Reportar Bug](https://img.shields.io/badge/🐛%20Reportar%20Bug-FF6B6B?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/issues/new?assignees=&labels=bug%2Ctriage&template=bug_report.yml&title=%5BBUG%5D%3A+)
[![Nueva Funcionalidad](https://img.shields.io/badge/✨%20Nueva%20Funcionalidad-4ECDC4?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/issues/new?assignees=&labels=enhancement%2Ctriage&template=feature_request.yml&title=%5BFEATURE%5D%3A+)
[![Hacer Pregunta](https://img.shields.io/badge/❓%20Hacer%20Pregunta-45B7D1?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/issues/new?assignees=&labels=question%2Ctriage&template=question.yml&title=%5BPREGUNTA%5D%3A+)
[![Mejorar Documentación](https://img.shields.io/badge/📖%20Mejorar%20Docs-96CEB4?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/issues/new?assignees=&labels=documentation%2Ctriage&template=documentation.yml&title=%5BDOCS%5D%3A+)

### **🚀 Enlaces Directos**

[![Issues Abiertos](https://img.shields.io/github/issues/Chicook/WoldVirtual_Crypto_3Dv1?style=flat-square&color=red&logo=github)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/Chicook/WoldVirtual_Crypto_3Dv1?style=flat-square&color=blue&logo=github)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/pulls)
[![Discusiones](https://img.shields.io/badge/💬%20Discusiones-Join-purple?style=flat-square&logo=github)](https://github.com/Chicook/WoldVirtual_Crypto_3Dv1/discussions)
[![Proyecto](https://img.shields.io/badge/📊%20Proyecto-View-orange?style=flat-square&logo=github)](https://github.com/users/Chicook/projects)

</div>

### **📝 Templates para Issues**

## 🏗️ Arquitectura Principal

```
WoldVirtual.0.0.1/
├── 📄 readme.md                    # Documentación principal del proyecto
├── 📄 ESTRUCTURA_PROYECTO.md       # Este archivo - Guía de estructura
├── 📄 Organización.md              # Documentación de organización interna
├── 📄 LICENSE                      # Licencia MIT del proyecto
├── 📄 .gitignore                   # Archivos ignorados por Git
├── 📁 .github/                     # Configuración de GitHub (workflows, etc.)
├── 📁 bakup/                       # Sistema de copias de seguridad
├── 📁 v.0.0.25/                    # Versión anterior del proyecto
├── 📁 frontend/                    # Interfaz de usuario y componentes
├── 📁 baquend/                     # Backend y lógica del servidor
├── 📁 public/                      # Archivos públicos y estáticos
├── 📁 pruebas/                     # Pruebas de desarrollo manual
├── 📁 tests/                       # Suite de pruebas automatizadas
└── 📁 pytest.ini/                  # Configuración de pytest
```

## 📂 Descripción Detallada de Carpetas

### 🔧 `.github/`
**Propósito**: Configuración de GitHub y CI/CD
- Workflows de GitHub Actions
- Templates para issues y pull requests
- Configuración de dependabot
- Configuración de seguridad

### 💾 `bakup/`
**Propósito**: Sistema de copias de seguridad
```
bakup/
├── 📁 copia_de_seguridad/          # Backup principal del proyecto
│   ├── 📁 WoldVirtual_Crypto_3D/   # Proyecto principal
│   ├── 📁 components/              # Componentes reutilizables
│   ├── 📁 services/                # Servicios del sistema
│   └── 📁 utils/                   # Utilidades y helpers
└── 📁 recuperacion/                # Scripts de recuperación
```

### 📚 `v.0.0.25/`
**Propósito**: Versión anterior del proyecto (archivada)
- Contiene la versión anterior completa
- Útil para comparaciones y recuperación
- No se modifica activamente

### 🎨 `frontend/`
**Propósito**: Interfaz de usuario y componentes frontend
```
frontend/
├── 📁 components/                  # Componentes React/Vue
├── 📁 pages/                       # Páginas de la aplicación
├── 📁 assets/                      # Imágenes, CSS, JS
├── 📁 styles/                      # Estilos y temas
└── 📄 package.json                 # Dependencias de frontend
```

### ⚙️ `baquend/`
**Propósito**: Backend y lógica del servidor
```
baquend/
├── 📁 api/                         # Endpoints de la API
├── 📁 models/                      # Modelos de datos
├── 📁 services/                    # Lógica de negocio
├── 📁 database/                    # Configuración de base de datos
└── 📄 app.py                       # Aplicación principal
```

### 🌐 `public/`
**Propósito**: Archivos públicos y estáticos
```
public/
├── 📁 assets/                      # Recursos estáticos
├── 📁 images/                      # Imágenes públicas
├── 📁 documents/                   # Documentos públicos
└── 📄 index.html                   # Página principal
```

### 🧪 `pruebas/`
**Propósito**: Pruebas de desarrollo manual
- Pruebas exploratorias
- Scripts de testing manual
- Casos de uso específicos
- Debugging y troubleshooting

### ✅ `tests/`
**Propósito**: Suite de pruebas automatizadas
```
tests/
├── 📄 test_hello_world.py          # Pruebas básicas
├── 📄 test_woldvirtual.py          # Pruebas del proyecto principal
├── 📄 conftest.py                  # Configuración de pytest
└── 📁 integration/                 # Pruebas de integración
```

### ⚙️ `pytest.ini/`
**Propósito**: Configuración de pytest
- Configuración de test discovery
- Opciones de ejecución
- Configuración de reportes
- Configuración de cobertura

## 🗂️ Navegación por el Proyecto

### 🚀 Para Desarrolladores Nuevos

1. **Comienza con**: `readme.md` - Documentación principal
2. **Revisa**: `ESTRUCTURA_PROYECTO.md` - Este archivo
3. **Explora**: `frontend/` y `baquend/` - Código principal
4. **Prueba**: `tests/` - Ejecuta las pruebas

### 🔍 Para Encontrar Código Específico

- **Frontend**: `frontend/components/`
- **Backend**: `baquend/api/`
- **Base de datos**: `baquend/models/`
- **Pruebas**: `tests/`
- **Configuración**: Archivos en la raíz

### 🛠️ Para Desarrollo

- **Nuevas características**: `frontend/` o `baquend/`
- **Pruebas**: `tests/`
- **Documentación**: Archivos `.md` en la raíz
- **Configuración**: Archivos de configuración en cada carpeta

## 📋 Convenciones de Nomenclatura

### 📁 Carpetas
- **Minúsculas** con guiones bajos: `copia_de_seguridad`
- **Descriptivas**: `frontend`, `baquend`, `tests`
- **Consistentes**: Seguir patrones establecidos

### 📄 Archivos
- **Python**: `snake_case.py`
- **JavaScript**: `camelCase.js`
- **CSS**: `kebab-case.css`
- **Documentación**: `PascalCase.md`

### 🏷️ Variables y Funciones
- **Python**: `snake_case`
- **JavaScript**: `camelCase`
- **Constantes**: `UPPER_CASE`

## 🔄 Flujo de Trabajo

### 📥 Desarrollo
1. Crear rama desde `WoldVirtual.0.0.1`
2. Trabajar en `frontend/` o `baquend/`
3. Añadir pruebas en `tests/`
4. Actualizar documentación

### ✅ Testing
1. Ejecutar `pytest` en `tests/`
2. Verificar cobertura de código
3. Probar manualmente en `pruebas/`
4. Validar integración

### 📤 Despliegue
1. Merge a rama principal
2. Ejecutar pruebas completas
3. Desplegar desde `public/`
4. Actualizar documentación

## 🎯 Próximos Pasos

### 🔧 Mejoras de Estructura
- [ ] Organizar mejor `frontend/` con subcarpetas
- [ ] Estandarizar estructura de `baquend/`
- [ ] Mejorar documentación de cada carpeta
- [ ] Crear guías de contribución específicas

### 📚 Documentación
- [ ] README específico para cada carpeta principal
- [ ] Guías de desarrollo paso a paso
- [ ] Documentación de API
- [ ] Ejemplos de uso

---

**Nota**: Esta estructura está diseñada para ser escalable y mantenible. Si necesitas hacer cambios, asegúrate de actualizar esta documentación.

*Última actualización: Junio 21, 2025* 
