# Modelos de WoldVirtual Crypto 3D

Este directorio contiene los modelos de datos principales del metaverso WoldVirtual Crypto 3D, refactorizados para mayor eficiencia, consistencia y mejores prácticas.

## Estructura del Directorio

```
models/
├── user.py          # Modelo de usuario con gestión de wallet y reputación
├── asset.py         # Modelo de activo digital (NFT) con metadatos completos
├── scene.py         # Modelo de escena 3D con gestión de contenido
└── transaction.py   # Modelo de transacción blockchain con estados completos
```

## Mejoras Implementadas

### 🔧 Refactorización General
- **Enums tipados**: Uso de `Enum` para tipos y estados
- **Validación de datos**: Validación automática en `__init__`
- **Campos por defecto**: Uso de `field(default_factory=...)` para objetos mutables
- **Timestamps UTC**: Uso consistente de `datetime.utcnow()`
- **Índices de base de datos**: Optimización de consultas
- **Tipado mejorado**: Anotaciones de tipo completas
- **Documentación**: Docstrings detallados para todos los métodos

### 📊 Métricas y Analytics
- **Scores de popularidad**: Cálculo automático basado en métricas
- **Tiempo de confirmación**: Tracking de transacciones blockchain
- **Complejidad de escenas**: Score basado en assets y objetos
- **Actividad de usuarios**: Tracking de engagement

## Modelos Principales

### 1. Usuario (`user.py`)
Modelo completo de usuario con gestión de wallet, reputación y actividad.

#### Características Principales
- **Gestión de wallet**: Verificación y conexión de wallets
- **Sistema de reputación**: Score ponderado con suavizado
- **Inventario dinámico**: Assets y escenas poseídas/creadas
- **Configuración de privacidad**: Control granular de visibilidad
- **Métricas financieras**: Tracking de ganancias y gastos
- **Actividad temporal**: Timestamps de login y actividad

#### Atributos Clave
```python
# Información básica
username: str                    # Nombre único
email: str                       # Email válido
wallet_address: str              # Dirección Ethereum

# Estado y actividad
is_active: bool                  # Estado de la cuenta
is_verified: bool                # Verificación de wallet
is_premium: bool                 # Estado premium
last_login: datetime             # Último acceso

# Inventario
owned_assets: List[str]          # Assets poseídos
created_scenes: List[str]        # Escenas creadas
favorite_scenes: List[str]       # Escenas favoritas

# Métricas
reputation_score: float          # Score de reputación
total_earnings: float            # Ganancias totales
total_spent: float               # Gastos totales
```

#### Métodos Principales
- `verify_wallet()`: Verificación criptográfica
- `update_reputation()`: Actualización de reputación
- `add_earnings()/add_expense()`: Tracking financiero
- `get_public_profile()`: Perfil público
- `is_new_user`/`has_activity`: Properties de estado

### 2. Activo Digital (`asset.py`)
Modelo completo de NFT con gestión de metadatos, mercado y blockchain.

#### Características Principales
- **Tipos de activos**: Enum con categorías específicas
- **Estados de publicación**: Draft, Published, Archived, Deleted
- **Información técnica**: Dimensiones, polígonos, formatos
- **Sistema de licencias**: Tipos de licencia comercial/personal
- **Regalías automáticas**: Porcentaje configurable
- **Metadatos NFT**: Compatible con estándares OpenSea

#### Enums Definidos
```python
class AssetType(str, Enum):
    MODEL_3D = "3d_model"
    TEXTURE = "texture"
    SOUND = "sound"
    ANIMATION = "animation"
    SCENE = "scene"
    CHARACTER = "character"
    VEHICLE = "vehicle"
    BUILDING = "building"
    NATURE = "nature"
    EFFECT = "effect"

class AssetStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

#### Métodos Principales
- `publish()/archive()/delete()`: Gestión de estados
- `set_technical_info()`: Información técnica
- `transfer_ownership()`: Transferencia de propiedad
- `get_nft_metadata()`: Metadatos para blockchain
- `popularity_score`: Score de popularidad

### 3. Escena 3D (`scene.py`)
Modelo avanzado de escena con gestión de contenido, acceso y rendimiento.

#### Características Principales
- **Tipos de escena**: Game, Experience, Gallery, Meeting, Event
- **Control de acceso**: Public, Private, Whitelist, Token-gated
- **Gestión de assets**: Transformaciones y posicionamiento
- **Métricas de rendimiento**: Complejidad y optimización
- **Tiempo de juego**: Tracking de engagement
- **Configuración de red**: Máximo de jugadores simultáneos

#### Enums Definidos
```python
class SceneType(str, Enum):
    GAME = "game"
    EXPERIENCE = "experience"
    GALLERY = "gallery"
    MEETING = "meeting"
    EVENT = "event"
    SHOWROOM = "showroom"

class SceneStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

#### Métodos Principales
- `add_asset()/remove_asset()`: Gestión de contenido
- `update_asset_transform()`: Posicionamiento dinámico
- `check_access_permission()`: Control de acceso
- `calculate_complexity_score()`: Score de complejidad
- `get_scene_data()`: Datos para renderizado
- `average_playtime`: Tiempo promedio de juego

### 4. Transacción (`transaction.py`)
Modelo completo de transacción blockchain con gestión de estados y fees.

#### Características Principales
- **Tipos de transacción**: Purchase, Sale, Transfer, Mint, Burn, Bid
- **Estados completos**: Pending, Confirmed, Failed, Cancelled, Expired
- **Información de gas**: Tracking de costos de transacción
- **Fees automáticos**: Platform fees y creator royalties
- **Metadatos blockchain**: Información completa de red
- **Timestamps específicos**: Confirmación y fallo

#### Enums Definidos
```python
class TransactionType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    TRANSFER = "transfer"
    MINT = "mint"
    BURN = "burn"
    BID = "bid"
    ACCEPT_BID = "accept_bid"
    ROYALTY = "royalty"
    REFUND = "refund"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
```

#### Métodos Principales
- `confirm_transaction()`: Confirmación con datos de bloque
- `fail_transaction()/cancel_transaction()`: Gestión de errores
- `set_fees()`: Configuración de comisiones
- `calculate_total_amount()`: Monto total con fees
- `get_blockchain_info()`: Información de blockchain
- `confirmation_time`: Tiempo de confirmación

## Relaciones y Validaciones

### 🔗 Relaciones entre Modelos
1. **Usuario ↔ Activo**: Propiedad y creación
2. **Usuario ↔ Escena**: Creación y favoritos
3. **Escena ↔ Activo**: Contenido y assets
4. **Transacción**: Conecta todos los modelos

### ✅ Validaciones Implementadas
- **Datos requeridos**: Validación de campos obligatorios
- **Formato de wallet**: Direcciones Ethereum válidas
- **Precios positivos**: Validación de montos
- **Estados válidos**: Transiciones de estado permitidas
- **Relaciones únicas**: Prevención de duplicados

## Optimizaciones de Base de Datos

### 📈 Índices Configurados
```python
# Usuario
indexes = [
    ("username",),
    ("email",),
    ("wallet_address",),
    ("is_active",),
    ("reputation_score",)
]

# Activo
indexes = [
    ("creator_id",),
    ("asset_type",),
    ("status",),
    ("is_public",),
    ("is_for_sale",),
    ("price",),
    ("created_at",),
    ("views",)
]

# Escena
indexes = [
    ("creator_id",),
    ("scene_type",),
    ("status",),
    ("is_public",),
    ("is_for_sale",),
    ("access_type",),
    ("created_at",),
    ("views",),
    ("complexity_score",)
]

# Transacción
indexes = [
    ("transaction_hash",),
    ("sender_id",),
    ("receiver_id",),
    ("transaction_type",),
    ("status",),
    ("created_at",),
    ("asset_id",),
    ("scene_id",),
    ("block_number",)
]
```

## Métodos de Utilidad

### 📊 Métricas y Analytics
- **Popularity Score**: Cálculo basado en vistas, likes, descargas
- **Complexity Score**: Basado en assets, objetos y dimensiones
- **Confirmation Time**: Tiempo de confirmación de transacciones
- **Average Playtime**: Tiempo promedio de juego por escena

### 🔍 Búsqueda y Filtrado
- **Tags normalizados**: Conversión a minúsculas
- **Categorías**: Organización jerárquica
- **Estados**: Filtrado por estado de publicación
- **Tipos**: Filtrado por tipo de contenido

### 📱 APIs Públicas
- `get_public_profile()`: Perfil público de usuario
- `get_public_info()`: Información pública de activo/escena
- `get_transaction_summary()`: Resumen de transacción
- `get_nft_metadata()`: Metadatos para blockchain

## Buenas Prácticas Implementadas

### 🛡️ Seguridad
- Validación de datos en `__init__`
- Verificación de permisos de acceso
- Sanitización de inputs
- Control de estados de transacción

### ⚡ Rendimiento
- Índices optimizados para consultas frecuentes
- Cálculo lazy de métricas complejas
- Uso de properties para cálculos dinámicos
- Timestamps UTC para consistencia

### 🔧 Mantenibilidad
- Enums para tipos y estados
- Métodos con responsabilidad única
- Documentación completa
- Validaciones centralizadas

### 📈 Escalabilidad
- Diseño para alta concurrencia
- Separación de metadatos
- Configuración flexible
- Extensibilidad de tipos 