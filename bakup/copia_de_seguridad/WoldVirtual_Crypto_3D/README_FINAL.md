# 🚀 WoldVirtual Crypto 3D - Metaverso Descentralizado 3D

## 📋 Descripción

WoldVirtual Crypto 3D es un metaverso descentralizado completo con capacidades de criptomonedas, renderizado 3D en tiempo real, y una interfaz web moderna construida con Reflex. El proyecto integra blockchain, Three.js, y una arquitectura modular escalable.

## 🎯 Características Principales

- **🌐 Interfaz Web Moderna**: Construida con Reflex y Tailwind CSS
- **🎨 Renderizado 3D**: Integración completa con Three.js
- **💰 Blockchain Integration**: Soporte multi-cadena (Ethereum, Polygon, BSC, etc.)
- **🏗️ Arquitectura Modular**: Componentes reutilizables y escalables
- **🔐 Seguridad Avanzada**: Autenticación, validación y encriptación
- **📊 Marketplace**: Compra/venta de assets con criptomonedas
- **🎮 Escenas Interactivas**: Física, animaciones y colaboración en tiempo real
- **📱 Responsive Design**: Funciona en desktop, tablet y móvil

## 🚀 Inicio Rápido

### Opción 1: Botón de Encendido (Recomendado)

```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Python directo
python WoldVirtual_Crypto_3D.py
```

### Opción 2: Instalación Manual

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd WoldVirtual_Crypto_3D

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 4. Ejecutar
python WoldVirtual_Crypto_3D.py
```

### Opción 3: Con Docker

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

## 📁 Estructura del Proyecto

```
WoldVirtual_Crypto_3D/
├── 🚀 WoldVirtual_Crypto_3D.py    # Botón de encendido principal
├── ⚙️ rxconfig.py                 # Configuración de Reflex
├── 🧠 state.py                    # Estado global de la aplicación
├── 📄 pages.py                    # Páginas y rutas
├── 🔧 init_reflex.py              # Script de inicialización
├── 📦 requirements.txt            # Dependencias de Python
├── 🌍 .env                        # Variables de entorno
├── 🐳 Dockerfile                  # Configuración de Docker
├── 🐳 docker-compose.yml          # Servicios de Docker
├── 🛠️ Makefile                    # Comandos útiles
├── 🚀 start.bat                   # Script de lanzamiento Windows
├── 🚀 start.sh                    # Script de lanzamiento Linux/Mac
├── 📚 README_FINAL.md             # Este archivo
├── 📚 REFLEX_SETUP.md             # Documentación de Reflex
├── 📚 docs/                       # Documentación completa
├── 🎨 assets/                     # Assets estáticos
│   ├── models/                    # Modelos 3D
│   ├── textures/                  # Texturas
│   ├── sounds/                    # Audio
│   └── animations/                # Animaciones
├── 🧩 components/                 # Componentes reutilizables
│   ├── navbar.py                  # Barra de navegación
│   ├── scene3d.py                 # Componente 3D
│   ├── marketplace.py             # Marketplace
│   ├── profile.py                 # Perfil de usuario
│   ├── explore.py                 # Exploración
│   ├── create.py                  # Creación de contenido
│   └── home.py                    # Página de inicio
├── 🗄️ models/                     # Modelos de datos
│   ├── user.py                    # Modelo de usuario
│   ├── asset.py                   # Modelo de asset
│   ├── scene.py                   # Modelo de escena
│   └── transaction.py             # Modelo de transacción
├── 🔧 utils/                      # Utilidades
│   ├── constants.py               # Constantes globales
│   ├── helpers.py                 # Funciones helper
│   ├── web3_utils.py              # Utilidades Web3
│   └── three_utils.py             # Utilidades Three.js
├── ⚙️ backend/                    # Backend y API
│   ├── database.py                # Configuración de BD
│   ├── models.py                  # Modelos de BD
│   ├── crud.py                    # Operaciones CRUD
│   ├── api/                       # Endpoints de API
│   └── utils.py                   # Utilidades del backend
├── 🎨 assets/                     # Gestores de assets
│   ├── asset_manager.py           # Gestor de assets
│   ├── scene_manager.py           # Gestor de escenas
│   ├── texture_manager.py         # Gestor de texturas
│   └── audio_manager.py           # Gestor de audio
├── 📜 contracts/                  # Contratos inteligentes
│   ├── ethereum/                  # Contratos Ethereum
│   ├── polygon/                   # Contratos Polygon
│   ├── bsc/                       # Contratos BSC
│   └── marketplace/               # Contratos de marketplace
├── 🧪 tests/                      # Tests
│   ├── unit/                      # Tests unitarios
│   ├── integration/               # Tests de integración
│   └── e2e/                       # Tests end-to-end
└── 📊 logs/                       # Archivos de log
```

## 🎮 Uso de la Aplicación

### 1. Inicio de Sesión
- Conectar wallet (MetaMask, WalletConnect, etc.)
- Seleccionar red blockchain
- Verificar balance

### 2. Exploración del Metaverso
- Navegar por escenas 3D
- Interactuar con objetos
- Chatear con otros usuarios
- Participar en eventos

### 3. Marketplace
- Comprar/vender assets
- Crear NFTs
- Participar en subastas
- Gestionar colecciones

### 4. Creación de Contenido
- Subir modelos 3D
- Crear texturas
- Diseñar escenas
- Publicar en marketplace

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Entorno
ENVIRONMENT=development
DEBUG_MODE=True
LOG_LEVEL=DEBUG

# Base de datos
DATABASE_URL=sqlite:///woldvirtual.db

# API
API_HOST=localhost
API_PORT=8000
FRONTEND_PORT=3000

# Web3
WEB3_PROVIDER_URL=http://localhost:8545
WEB3_CHAIN_ID=1

# Seguridad
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Contratos
NFT_CONTRACT_ADDRESS=
MARKETPLACE_CONTRACT_ADDRESS=
```

### Configuración de Redes Blockchain

El proyecto soporta múltiples redes:

- **Ethereum Mainnet** (Chain ID: 1)
- **Polygon** (Chain ID: 137)
- **BSC** (Chain ID: 56)
- **Arbitrum** (Chain ID: 42161)
- **Optimism** (Chain ID: 10)
- **Avalanche** (Chain ID: 43114)

## 🛠️ Desarrollo

### Comandos Útiles

```bash
# Desarrollo
make dev
# o
reflex run

# Tests
make test
# o
pytest tests/ -v --cov=.

# Construir
make build
# o
reflex export

# Desplegar
make deploy
# o
reflex deploy

# Limpiar
make clean

# Docker
make docker-up
make docker-down
make docker-logs
```

### Estructura de Desarrollo

```python
# Ejemplo de componente
def MyComponent() -> rx.Component:
    return rx.box(
        rx.text("Mi Componente"),
        rx.button("Acción", on_click=State.my_action),
        background="white",
        padding="4",
    )

# Ejemplo de estado
class State(rx.State):
    count: int = 0
    
    def increment(self):
        self.count += 1
```

## 🧪 Testing

### Tests Unitarios

```python
def test_user_creation():
    user = User(
        username="test_user",
        email="test@example.com",
        wallet_address="0x123..."
    )
    assert user.username == "test_user"
    assert user.is_active == True
```

### Tests de Integración

```python
def test_wallet_connection():
    state = WoldVirtualState()
    state.connect_wallet()
    assert state.wallet_connected == True
    assert state.is_authenticated == True
```

## 🚀 Despliegue

### Desarrollo Local

```bash
python WoldVirtual_Crypto_3D.py
```

### Producción con Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Despliegue en la Nube

```bash
# Reflex Cloud
reflex deploy

# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

## 📊 Monitoreo

### Métricas Disponibles

- Usuarios activos
- Transacciones blockchain
- Rendimiento de escenas 3D
- Errores y excepciones
- Uso de recursos

### Health Checks

```bash
# Verificar estado del sistema
curl http://localhost:8000/health

# Verificar métricas
curl http://localhost:8000/metrics
```

## 🔒 Seguridad

### Características de Seguridad

- ✅ Validación de entrada
- ✅ Autenticación JWT
- ✅ Encriptación de datos
- ✅ Validación de firmas blockchain
- ✅ Rate limiting
- ✅ CORS configurado
- ✅ Content Security Policy

### Mejores Prácticas

- Usar variables de entorno para secretos
- Validar todas las entradas de usuario
- Implementar rate limiting
- Mantener dependencias actualizadas
- Usar HTTPS en producción

## 🤝 Contribución

### Cómo Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa tus cambios
4. Añade tests
5. Documenta los cambios
6. Abre un Pull Request

### Estándares de Código

- Usar Black para formateo
- Seguir PEP 8
- Documentar funciones y clases
- Escribir tests para nuevas funcionalidades
- Usar type hints

## 📚 Recursos

### Documentación

- [Documentación de Reflex](https://reflex.dev/docs)
- [Documentación de Web3.py](https://web3py.readthedocs.io/)
- [Documentación de Three.js](https://threejs.org/docs/)
- [Guía de Blockchain](https://ethereum.org/developers/)

### Comunidad

- 📧 Email: support@woldvirtual.com
- 💬 Discord: [WoldVirtual Community](https://discord.gg/woldvirtual)
- 📖 Documentación: [docs.woldvirtual.com](https://docs.woldvirtual.com)
- 🐛 Issues: [GitHub Issues](https://github.com/woldvirtual/issues)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🎉 ¡Gracias!

¡Gracias por usar WoldVirtual Crypto 3D! Esperamos que disfrutes explorando el metaverso descentralizado.

---

**🚀 ¡Listo para explorar el futuro del metaverso! 🚀** 