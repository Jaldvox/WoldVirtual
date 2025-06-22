# Configuración de Reflex para WoldVirtual Crypto 3D

## 🚀 Inicio Rápido

### 1. Instalación Automática

```bash
# Clonar el repositorio
git clone <repository-url>
cd WoldVirtual_Crypto_3D

# Ejecutar script de inicialización
python init_reflex.py
```

### 2. Instalación Manual

```bash
# Instalar Reflex
pip install reflex

# Instalar dependencias
pip install -r requirements.txt

# Inicializar Reflex
reflex init

# Ejecutar en desarrollo
reflex run
```

## 📁 Estructura de Archivos

```
WoldVirtual_Crypto_3D/
├── rxconfig.py              # Configuración principal de Reflex
├── state.py                 # Estado global de la aplicación
├── pages.py                 # Páginas y rutas
├── init_reflex.py           # Script de inicialización
├── requirements.txt         # Dependencias de Python
├── .env                     # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── Dockerfile              # Configuración de Docker
├── docker-compose.yml      # Servicios de Docker
├── Makefile                # Comandos útiles
├── assets/                 # Assets estáticos
├── components/             # Componentes reutilizables
├── models/                 # Modelos de datos
├── utils/                  # Utilidades
├── logs/                   # Archivos de log
└── tests/                  # Tests
```

## ⚙️ Configuración

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
```

### Configuración de Reflex (rxconfig.py)

```python
config = rx.Config(
    app_name="WoldVirtual_Crypto_3D",
    app_version="0.0.9",
    env=rx.Env.DEV,
    debug=True,
    frontend_port=3000,
    backend_port=8000,
    db_url="sqlite:///woldvirtual.db",
    cors_allowed_origins=["http://localhost:3000"],
    tailwind=TAILWIND_CONFIG,
    plugins=["reflex_web3", "reflex_threejs", "reflex_auth"],
)
```

## 🎮 Uso

### Comandos Principales

```bash
# Desarrollo
make dev
# o
reflex run --host 0.0.0.0 --port 3000

# Construir para producción
make build
# o
reflex export

# Desplegar
make deploy
# o
reflex deploy

# Tests
make test
# o
pytest tests/ -v --cov=.

# Limpiar
make clean
```

### Docker

```bash
# Levantar servicios
make docker-up
# o
docker-compose up -d

# Ver logs
make docker-logs
# o
docker-compose logs -f

# Detener servicios
make docker-down
# o
docker-compose down
```

## 🏗️ Arquitectura

### Estado Global (state.py)

```python
class WoldVirtualState(rx.State):
    # Estado de la aplicación
    app_loaded: bool = False
    current_page: str = "home"
    loading: bool = False
    
    # Estado del usuario
    is_authenticated: bool = False
    username: str = ""
    wallet_address: str = ""
    
    # Estado de escenas 3D
    current_scene_id: Optional[str] = None
    scene_loaded: bool = False
    camera_position: List[float] = [0, 5, 10]
    
    # Estado de blockchain
    web3_connected: bool = False
    network_id: int = 1
    wallet_balance: float = 0.0
```

### Páginas (pages.py)

```python
def MainPage() -> rx.Component:
    return rx.box(
        Navbar(),
        rx.cond(
            WoldVirtualState.current_page == "home",
            Home(),
            rx.cond(
                WoldVirtualState.current_page == "explore",
                Explore(),
                # ... más páginas
            )
        ),
        Sidebar(),
        Notifications(),
    )
```

## 🔧 Componentes

### Navbar
- Navegación principal
- Conexión de wallet
- Selector de red blockchain
- Notificaciones

### Scene3D
- Renderizado Three.js
- Controles de cámara
- Gestión de assets 3D
- Física y animaciones

### Marketplace
- Lista de assets
- Filtros y búsqueda
- Compra con criptomonedas
- Gestión de transacciones

### Profile
- Información del usuario
- Assets propios
- Configuración
- Estadísticas

## 🌐 Integración Web3

### Conexión de Wallet

```python
def connect_wallet(self):
    """Conecta la wallet del usuario."""
    try:
        self.loading = True
        # Implementación de conexión Web3
        self.wallet_connected = True
        self.wallet_address = "0x123..."
        self.is_authenticated = True
        self.loading = False
    except Exception as e:
        self.error_message = f"Error: {str(e)}"
```

### Transacciones

```python
def purchase_asset(self, asset_id: str, price: float):
    """Compra un asset del marketplace."""
    try:
        # Implementación de transacción blockchain
        self.user_owned_assets.append({
            "id": asset_id,
            "purchase_date": datetime.now().isoformat(),
            "price": price
        })
    except Exception as e:
        self.error_message = f"Error: {str(e)}"
```

## 🎨 Three.js Integration

### Configuración de Escena

```python
def load_scene(self, scene_id: str):
    """Carga una escena 3D."""
    self.current_scene_id = scene_id
    self.scene_loaded = False
    self.scene_loading_progress = 0.0
    
    # Configuración de Three.js
    scene_config = {
        "background": "#000000",
        "camera": {
            "fov": 75,
            "position": [0, 5, 10],
            "look_at": [0, 0, 0]
        },
        "lighting": {
            "ambient": {"color": "#ffffff", "intensity": 0.5},
            "directional": {"color": "#ffffff", "intensity": 0.8}
        }
    }
```

### Gestión de Assets

```python
def load_asset(self, asset_id: str, asset_type: str = "model"):
    """Carga un asset en la escena."""
    self.loaded_assets[asset_id] = {
        "id": asset_id,
        "type": asset_type,
        "loaded": True,
        "position": [0, 0, 0],
        "rotation": [0, 0, 0],
        "scale": [1, 1, 1]
    }
```

## 🧪 Testing

### Tests Unitarios

```python
def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False

def test_format_balance():
    assert format_balance("1000000000000000000") == "1.0000"
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
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar
reflex run
```

### Producción con Docker

```bash
# Construir imagen
docker build -t woldvirtual .

# Ejecutar contenedor
docker run -p 3000:3000 -p 8000:8000 woldvirtual
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

## 🔍 Debugging

### Logs

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Mensaje informativo")
logger.error("Error en la aplicación")
```

### Estado de la Aplicación

```python
def export_state(self) -> Dict[str, Any]:
    """Exporta el estado para debugging."""
    return {
        "user": {
            "authenticated": self.is_authenticated,
            "wallet_address": self.wallet_address
        },
        "scene": {
            "current": self.current_scene_id,
            "loaded": self.scene_loaded
        }
    }
```

## 📊 Monitoreo

### Métricas

- Usuarios activos
- Transacciones blockchain
- Rendimiento de escenas 3D
- Errores y excepciones

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.0.9"
    }
```

## 🔒 Seguridad

### Validación de Entrada

```python
def validate_wallet_address(address: str) -> bool:
    """Valida una dirección de wallet."""
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))
```

### Autenticación

```python
def authenticate_user(token: str) -> Optional[Dict]:
    """Autentica un usuario con JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
```

## 📚 Recursos Adicionales

- [Documentación de Reflex](https://reflex.dev/docs)
- [Documentación de Web3.py](https://web3py.readthedocs.io/)
- [Documentación de Three.js](https://threejs.org/docs/)
- [Guía de Blockchain](https://ethereum.org/developers/)

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- 📧 Email: support@woldvirtual.com
- 💬 Discord: [WoldVirtual Community](https://discord.gg/woldvirtual)
- 📖 Documentación: [docs.woldvirtual.com](https://docs.woldvirtual.com)
- 🐛 Issues: [GitHub Issues](https://github.com/woldvirtual/issues) 