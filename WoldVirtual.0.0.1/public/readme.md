# 🌌 MetaversoCryptoWoldVirtual - Backend Core
### Motor Principal del Metaverso WoldVirtual Crypto 3D

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Reflex](https://img.shields.io/badge/Reflex-0.4+-FF4B4B?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Backend_Core-success?style=for-the-badge)

</div>

---

## 📍 Ubicación en el Ecosistema

```
WoldVirtual_Crypto_3Dv1/
└── WoldVirtual.0.0.1/                    # Proyecto Python principal
    └── public/
        └── MetaversoCryptoWoldVirtual/   # ← ESTA SECCIÓN
            └── rxconfig.py               # Configuración principal
```

**Esta es la configuración central del backend Python que potencia todo el metaverso.**

---

## 🚀 Pasos de Instalación y Configuración

### **Paso 1: Preparar el Entorno**

```bash
# 1. Navegar a la carpeta del proyecto backend
cd WoldVirtual.0.0.1

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Verificar que Python esté disponible
python --version
# Debe mostrar Python 3.8 o superior
```

### **Paso 2: Instalar Dependencias**

```bash
# 1. Actualizar pip
python -m pip install --upgrade pip

# 2. Instalar Reflex (framework principal)
pip install reflex

# 3. Instalar dependencias adicionales para Web3 y blockchain
pip install web3 sqlalchemy python-dotenv requests aiohttp

# 4. Verificar instalación de Reflex
reflex --version
# Debe mostrar la versión instalada
```

### **Paso 3: Configurar Variables de Entorno (Opcional)**

Crea un archivo `.env` en la carpeta `WoldVirtual.0.0.1/`:

```bash
# Archivo: WoldVirtual.0.0.1/.env
ENVIRONMENT=development
DEBUG_MODE=True
API_HOST=localhost
API_PORT=8000
FRONTEND_PORT=3000
DATABASE_URL=sqlite:///woldvirtual_crypto_3d.db
```

### **Paso 4: Verificar Configuración**

```bash
# 1. Navegar a la carpeta de configuración
cd public/MetaversoCryptoWoldVirtual

# 2. Verificar que rxconfig.py existe y es válido
python -c "import rxconfig; print('✅ Configuración válida')"

# 3. Verificar las variables de configuración
python -c "from rxconfig import EnvironmentConfig; print(f'App: {EnvironmentConfig.APP_NAME}, Puerto: {EnvironmentConfig.API_PORT}')"
```

### **Paso 5: Inicializar Proyecto Reflex**

```bash
# 1. Volver a la carpeta raíz del backend
cd ../../  # Desde MetaversoCryptoWoldVirtual hacia WoldVirtual.0.0.1

# 2. Inicializar Reflex (esto detectará automáticamente rxconfig.py)
reflex init

# 3. Esto creará automáticamente:
# - .web/ (archivos de compilación)
# - requirements.txt (si no existe)
# - Estructura de frontend compilada
```

### **Paso 6: Ejecutar el Backend**

```bash
# 1. Ejecutar servidor de desarrollo
reflex run

# 2. Si todo está correcto, verás:
# ✅ Salida esperada:
# ── Wold Virtual Crypto 3D ─────────────────────────
# 🚀 WoldVirtual Crypto 3D v0.0.9
# 🌍 Entorno: development
# 🔧 Debug: True
# 🌐 Frontend: http://localhost:3000
# ⚙️  Backend: http://localhost:8000
# 💾 Database: sqlite:///woldvirtual_crypto_3d.db
# ══════════════════════════════════════════════════

# 3. El navegador se abrirá automáticamente en:
# http://localhost:3000
```

---

## 🔧 Configuración Avanzada

### **📊 Variables de Entorno Disponibles**

| **Variable** | **Valor por Defecto** | **Descripción** |
|-------------|----------------------|-----------------|
| `ENVIRONMENT` | `development` | Entorno de ejecución |
| `DEBUG_MODE` | `True` | Modo debug activado |
| `API_HOST` | `localhost` | Host del API |
| `API_PORT` | `8000` | Puerto del backend |
| `FRONTEND_PORT` | `3000` | Puerto del frontend |
| `DATABASE_URL` | `sqlite:///woldvirtual_crypto_3d.db` | URL de base de datos |

### **🌐 Puertos Configurados**

- **Backend API**: http://localhost:8000
- **Frontend Reflex**: http://localhost:3000
- **React Component**: http://localhost:5173 (CORS habilitado)

### **🎨 Colores del Tema Tailwind**

```css
/* Colores disponibles en la aplicación */
primary: #00ff00    /* Verde neón principal */
secondary: #0099ff  /* Azul cibernético */
accent: #ff6b35     /* Naranja de acento */
dark: #1a1a2e       /* Fondo oscuro */
darker: #16213e     /* Más oscuro */
```

---

## 🛠️ Comandos Útiles

### **Desarrollo**

```bash
# Iniciar servidor de desarrollo
reflex run

# Iniciar solo backend
reflex run --backend-only

# Iniciar solo frontend  
reflex run --frontend-only

# Limpiar archivos generados
reflex clean
```

### **Debugging**

```bash
# Verificar configuración
python -c "from public.MetaversoCryptoWoldVirtual.rxconfig import config; print(config.app_name)"

# Ver todas las configuraciones
python -c "from public.MetaversoCryptoWoldVirtual.rxconfig import *; print(f'CORS: {get_cors_origins()}')"

# Test de conexión de base de datos
python -c "from public.MetaversoCryptoWoldVirtual.rxconfig import EnvironmentConfig; print(f'DB: {EnvironmentConfig.DATABASE_URL}')"
```

### **Producción**

```bash
# Configurar para producción
export ENVIRONMENT=production
export DEBUG_MODE=False

# Compilar para producción
reflex export

# Los archivos compilados estarán en ./export/
```

---

## 🔍 Solución de Problemas

### **❌ Error: "No module named 'reflex'"**

```bash
# Solución: Reinstalar Reflex
pip install --upgrade reflex
```

### **❌ Error: "rxconfig.py not found"**

```bash
# Verificar ubicación
ls public/MetaversoCryptoWoldVirtual/rxconfig.py

# Si no existe, crear uno básico:
cd public/MetaversoCryptoWoldVirtual
cat > rxconfig.py << 'EOF'
import reflex as rx
config = rx.Config(app_name="WoldVirtual_Crypto_3D")
EOF
```

### **❌ Error: "Port already in use"**

```bash
# Cambiar puertos en .env o usar diferentes:
reflex run --frontend-port 3001 --backend-port 8001
```

### **❌ Error: Database connection**

```bash
# Verificar que la base de datos es accesible
python -c "import sqlite3; sqlite3.connect('woldvirtual_crypto_3d.db').close(); print('✅ DB OK')"
```

---

## 📚 Estructura de Archivos Generada

Después de ejecutar `reflex init` y `reflex run`:

```
WoldVirtual.0.0.1/
├── 📁 .web/                              # Archivos compilados (auto-generado)
├── 📁 public/
│   └── 📁 MetaversoCryptoWoldVirtual/
│       └── 📄 rxconfig.py               # ← Configuración principal
├── 📁 assets/                           # Recursos estáticos (auto-generado)
├── 📄 requirements.txt                  # Dependencias (auto-generado)
├── 📄 .gitignore                       # Git ignore (auto-generado)
└── 📄 woldvirtual_crypto_3d.db         # Base de datos SQLite
```

---

## 🔗 Integración con Otros Componentes

### **🎮 Con React Three.js**

El backend está configurado para CORS con:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Reflex frontend)

### **⛓️ Con Blockchain**

Variables preparadas para Web3:
- Soporte para múltiples chains
- Configuración de providers
- Integración con wallets

### **📊 Con Base de Datos**

- SQLite por defecto para desarrollo
- PostgreSQL/MySQL para producción
- Migraciones automáticas con SQLAlchemy

---

## 🎯 Próximos Pasos

Una vez que tengas el backend funcionando:

1. **✅ Backend corriendo**: `reflex run` exitoso
2. **🎮 Integrar React**: Conectar componente Three.js
3. **⛓️ Añadir Web3**: Integrar funcionalidades blockchain
4. **🗄️ Configurar DB**: Setup de base de datos avanzada
5. **🚀 Deploy**: Preparar para producción

---

## 🤝 Contribución

### **🐛 Reportar Issues**

Si encuentras problemas específicos con esta configuración:

1. **Verificar logs**: Revisar salida de `reflex run`
2. **Verificar dependencias**: `pip list | grep reflex`
3. **Verificar puertos**: `netstat -tulpn | grep :8000`

### **✨ Mejoras**

Las mejoras a esta configuración deben mantener:
- ✅ Compatibilidad con Reflex actual
- ✅ Soporte para desarrollo y producción
- ✅ Variables de entorno configurables
- ✅ CORS para integración React

---

<div align="center">

### **🚀 MetaversoCryptoWoldVirtual - El Motor del Futuro**

*Esta configuración es el corazón del backend que potencia toda la experiencia del metaverso WoldVirtual. Cada configuración está optimizada para desarrollo ágil y escalabilidad en producción.*

[![Verificar Config](https://img.shields.io/badge/🔧%20VERIFICAR%20CONFIG-success?style=for-the-badge)](https://localhost:8000)
[![Ver Logs](https://img.shields.io/badge/📊%20VER%20LOGS-info?style=for-the-badge)](https://localhost:8000/admin)

---

**Sección**: Backend Core Configuration  
**Parte de**: [WoldVirtual Crypto 3D Ecosystem](../../../README.md)  
**Versión**: 0.0.9 - Backend Funcional  
**Última Actualización**: Junio 22, 2025

</div>