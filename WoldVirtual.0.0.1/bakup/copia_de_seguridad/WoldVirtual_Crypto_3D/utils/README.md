# Carpeta Utils

## Descripción
Esta carpeta contiene utilidades, helpers y constantes que se utilizan en toda la aplicación WoldVirtual Crypto 3D. Proporciona funciones reutilizables para validación, formateo, conversiones, Web3, Three.js y otras operaciones comunes.

## Estructura de Archivos

### `constants.py`
- **Constantes globales** del sistema
- **Configuraciones** de desarrollo, producción y testing
- **Enumeraciones** para tipos de datos
- **Valores por defecto** para escenas, usuarios y assets
- **Configuraciones de red** y blockchain
- **Mensajes de error** estandarizados
- **Límites y restricciones** del sistema

### `helpers.py`
- **Funciones de validación** (email, wallet, username, password, archivos)
- **Funciones de formateo** (direcciones, balances, tamaños de archivo, timestamps)
- **Funciones de conversión** (wei/ETH, hex/int, bytes/hex)
- **Funciones de archivo** (extensiones, nombres únicos, sanitización)
- **Funciones de hash** y encriptación
- **Funciones de JSON** seguras
- **Funciones de limpieza** de datos
- **Utilidades generales** (chunks, flatten, deduplicación)

### `web3_utils.py`
- **Web3Manager**: Gestor principal de conexiones Web3
- **WalletManager**: Gestión de wallets y firmas
- **TransactionManager**: Envío y seguimiento de transacciones
- **SmartContractManager**: Interacción con contratos inteligentes
- **TokenUtils**: Utilidades para manejo de tokens
- **Funciones de utilidad** para redes blockchain
- **Validaciones** de direcciones y transacciones

### `three_utils.py`
- **Estructuras de datos** (Vector3, Quaternion, Transform)
- **GeometryUtils**: Creación de geometrías 3D
- **MaterialUtils**: Configuración de materiales
- **LightingUtils**: Configuración de iluminación
- **CameraUtils**: Configuración de cámaras
- **OptimizationUtils**: Optimización de rendimiento
- **AnimationUtils**: Configuración de animaciones
- **PhysicsUtils**: Configuración de física

## Uso

### Constantes
```python
from utils.constants import (
    DEFAULT_SCENE,
    CAMERA_SETTINGS,
    NETWORK_CONFIG,
    ASSET_TYPES,
    TransactionType,
    UserStatus
)

# Usar configuraciones por defecto
scene_config = DEFAULT_SCENE.copy()
camera_config = CAMERA_SETTINGS.copy()

# Usar enumeraciones
if transaction.type == TransactionType.PURCHASE:
    # Procesar compra
    pass
```

### Helpers
```python
from utils.helpers import (
    validate_email,
    validate_wallet_address,
    format_address,
    format_balance,
    wei_to_eth,
    generate_unique_filename,
    safe_json_loads
)

# Validaciones
if validate_email(user_email):
    # Email válido
    pass

if validate_wallet_address(wallet_address):
    # Wallet válida
    pass

# Formateo
formatted_address = format_address("0x1234567890abcdef1234567890abcdef12345678")
formatted_balance = format_balance("1000000000000000000")  # 1 ETH

# Conversiones
eth_amount = wei_to_eth("1000000000000000000")  # 1.0 ETH
wei_amount = eth_to_wei(1.5)  # 1500000000000000000

# Archivos
unique_name = generate_unique_filename("model.glb", prefix="asset")
```

### Web3 Utils
```python
from utils.web3_utils import (
    Web3Manager,
    WalletManager,
    TransactionManager,
    SmartContractManager
)

# Inicializar Web3
web3_manager = Web3Manager("https://mainnet.infura.io/v3/YOUR_KEY")

# Gestión de wallets
wallet_manager = WalletManager(web3_manager)
wallet_info = wallet_manager.create_wallet()
address = wallet_manager.import_wallet_from_private_key(private_key)

# Transacciones
tx_manager = TransactionManager(web3_manager)
tx_hash = tx_manager.send_eth_transaction(
    to_address="0x...",
    amount_eth=0.1,
    private_key=private_key
)

# Contratos inteligentes
contract_manager = SmartContractManager(web3_manager)
contract_manager.load_contract(contract_address, abi)
result = contract_manager.call_contract_function(
    contract_address, "balanceOf", user_address
)
```

### Three.js Utils
```python
from utils.three_utils import (
    Vector3,
    Transform,
    GeometryUtils,
    MaterialUtils,
    LightingUtils,
    CameraUtils
)

# Crear geometrías
box_geometry = GeometryUtils.create_box_geometry(1, 1, 1)
sphere_geometry = GeometryUtils.create_sphere_geometry(0.5)

# Crear materiales
basic_material = MaterialUtils.create_basic_material("#ff0000")
standard_material = MaterialUtils.create_standard_material(
    color="#ffffff",
    metalness=0.5,
    roughness=0.3
)

# Crear iluminación
ambient_light = LightingUtils.create_ambient_light("#ffffff", 0.5)
directional_light = LightingUtils.create_directional_light(
    color="#ffffff",
    intensity=1.0,
    position=Vector3(0, 10, 0)
)

# Crear cámara
camera = CameraUtils.create_perspective_camera(
    fov=75,
    position=Vector3(0, 5, 10),
    look_at=Vector3(0, 0, 0)
)
```

## Características Principales

### 🔧 Validación Robusta
- Validación de emails, wallets, usernames y contraseñas
- Validación de tipos de archivo y tamaños
- Validación de URLs y direcciones IP
- Validación de JSON y datos estructurados

### 💰 Integración Web3 Completa
- Gestión de conexiones blockchain
- Manejo de wallets y firmas
- Envío y seguimiento de transacciones
- Interacción con contratos inteligentes
- Soporte para múltiples redes

### 🎨 Utilidades 3D Avanzadas
- Estructuras de datos optimizadas para 3D
- Configuración de geometrías, materiales y luces
- Utilidades de cámara y animación
- Optimización de rendimiento
- Configuración de física

### 📊 Formateo y Conversión
- Formateo de direcciones blockchain
- Conversión de unidades (wei/ETH)
- Formateo de balances y tamaños
- Conversión de timestamps
- Sanitización de datos

### 🛡️ Seguridad
- Validación de firmas criptográficas
- Sanitización de nombres de archivo
- Validación de datos de entrada
- Manejo seguro de JSON
- Generación de hashes seguros

## Convenciones

### Nomenclatura
- **Funciones**: snake_case (ej: `validate_email`)
- **Clases**: PascalCase (ej: `Web3Manager`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `DEFAULT_SCENE`)
- **Enumeraciones**: PascalCase (ej: `TransactionType`)

### Documentación
- Todas las funciones deben tener docstrings
- Incluir ejemplos de uso en la documentación
- Documentar parámetros y valores de retorno
- Incluir información sobre excepciones

### Manejo de Errores
- Usar logging para errores importantes
- Retornar valores por defecto en caso de error
- Proporcionar mensajes de error descriptivos
- Validar entradas antes de procesar

### Rendimiento
- Usar funciones puras cuando sea posible
- Evitar operaciones costosas en bucles
- Implementar caché para operaciones repetitivas
- Optimizar consultas de base de datos

## Testing

### Cobertura de Tests
- **Validaciones**: 100% de cobertura
- **Conversiones**: 100% de cobertura
- **Web3**: Tests de integración
- **Three.js**: Tests unitarios de configuraciones

### Tipos de Tests
- **Unitarios**: Funciones individuales
- **Integración**: Interacción entre módulos
- **Edge Cases**: Casos límite y errores
- **Performance**: Rendimiento de funciones críticas

### Ejemplos de Tests
```python
def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    assert validate_email("") == False

def test_format_balance():
    assert format_balance("1000000000000000000") == "1.0000"
    assert format_balance("500000000000000000") == "0.5000"

def test_wei_to_eth():
    assert wei_to_eth("1000000000000000000") == 1.0
    assert wei_to_eth("500000000000000000") == 0.5
```

## Mantenimiento

### Actualizaciones
- Revisar dependencias regularmente
- Actualizar configuraciones según necesidades
- Mantener compatibilidad con versiones anteriores
- Documentar cambios importantes

### Optimización
- Monitorear rendimiento de funciones críticas
- Optimizar algoritmos cuando sea necesario
- Implementar caché para operaciones costosas
- Reducir complejidad de funciones complejas

### Seguridad
- Revisar funciones de validación regularmente
- Actualizar algoritmos de hash cuando sea necesario
- Verificar configuraciones de seguridad
- Mantener listas de valores permitidos actualizadas 