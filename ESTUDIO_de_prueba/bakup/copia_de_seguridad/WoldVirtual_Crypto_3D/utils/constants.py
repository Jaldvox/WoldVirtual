"""
Constantes globales para WoldVirtual Crypto 3D
Contiene configuraciones, valores por defecto y enumeraciones del sistema.
"""

from enum import Enum
from typing import Dict, List, Any
import os

# =============================================================================
# CONFIGURACIONES GLOBALES
# =============================================================================

# Configuración de la aplicación
APP_NAME = "WoldVirtual Crypto 3D"
APP_VERSION = "0.0.9"
APP_DESCRIPTION = "Metaverso descentralizado 3D con capacidades de criptomonedas"

# Configuración de desarrollo
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///woldvirtual.db")
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

# Configuración de API
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Configuración de Web3
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
WEB3_CHAIN_ID = int(os.getenv("WEB3_CHAIN_ID", "1"))  # Ethereum Mainnet
WEB3_GAS_LIMIT = int(os.getenv("WEB3_GAS_LIMIT", "300000"))
WEB3_GAS_PRICE = int(os.getenv("WEB3_GAS_PRICE", "20000000000"))  # 20 Gwei

# Configuración de IPFS
IPFS_GATEWAY = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs/")
IPFS_API_URL = os.getenv("IPFS_API_URL", "https://ipfs.infura.io:5001")
IPFS_TIMEOUT = int(os.getenv("IPFS_TIMEOUT", "30"))

# Configuración de Three.js
THREE_JS_VERSION = "0.158.0"
THREE_JS_CDN = f"https://cdnjs.cloudflare.com/ajax/libs/three.js/{THREE_JS_VERSION}/three.min.js"

# =============================================================================
# ENUMERACIONES
# =============================================================================

class AssetType(str, Enum):
    """Tipos de activos disponibles en el metaverso."""
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
    OTHER = "other"

class SceneType(str, Enum):
    """Tipos de escenas disponibles."""
    GAME = "game"
    EXPERIENCE = "experience"
    GALLERY = "gallery"
    MEETING = "meeting"
    EVENT = "event"
    SHOWROOM = "showroom"
    OTHER = "other"

class TransactionType(str, Enum):
    """Tipos de transacciones blockchain."""
    PURCHASE = "purchase"
    SALE = "sale"
    TRANSFER = "transfer"
    MINT = "mint"
    BURN = "burn"
    BID = "bid"
    ACCEPT_BID = "accept_bid"
    ROYALTY = "royalty"
    REFUND = "refund"
    OTHER = "other"

class TransactionStatus(str, Enum):
    """Estados de las transacciones."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class UserStatus(str, Enum):
    """Estados de los usuarios."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING_VERIFICATION = "pending_verification"

class AssetStatus(str, Enum):
    """Estados de los activos."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"

class SceneStatus(str, Enum):
    """Estados de las escenas."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"

class NetworkType(str, Enum):
    """Tipos de redes blockchain soportadas."""
    ETHEREUM_MAINNET = "ethereum_mainnet"
    ETHEREUM_TESTNET = "ethereum_testnet"
    POLYGON_MAINNET = "polygon_mainnet"
    POLYGON_TESTNET = "polygon_testnet"
    BSC_MAINNET = "bsc_mainnet"
    BSC_TESTNET = "bsc_testnet"
    ARBITRUM_ONE = "arbitrum_one"
    OPTIMISM = "optimism"

# =============================================================================
# CONFIGURACIONES DE ESCENA
# =============================================================================

# Configuración por defecto de escena
DEFAULT_SCENE = {
    "name": "Nueva Escena",
    "description": "Una nueva escena en el metaverso",
    "width": 1000,
    "height": 1000,
    "depth": 1000,
    "max_players": 50,
    "is_public": False,
    "is_template": False,
    "optimization_level": "medium"
}

# Configuración de cámara
CAMERA_SETTINGS = {
    "fov": 75,
    "near": 0.1,
    "far": 1000,
    "position": {"x": 0, "y": 5, "z": 10},
    "look_at": {"x": 0, "y": 0, "z": 0},
    "controls": {
        "enable_damping": True,
        "damping_factor": 0.05,
        "enable_zoom": True,
        "enable_rotate": True,
        "enable_pan": True
    }
}

# Configuración de iluminación
LIGHTING_SETTINGS = {
    "ambient": {
        "color": "#ffffff",
        "intensity": 0.5
    },
    "directional": {
        "color": "#ffffff",
        "intensity": 0.8,
        "position": {"x": 0, "y": 10, "z": 0},
        "cast_shadow": True
    },
    "hemisphere": {
        "sky_color": "#87ceeb",
        "ground_color": "#8b4513",
        "intensity": 0.3
    }
}

# Configuración de física
PHYSICS_SETTINGS = {
    "gravity": {"x": 0, "y": -9.81, "z": 0},
    "world_scale": 1.0,
    "solver_iterations": 10,
    "enable_debug": False,
    "materials": {
        "default": {
            "friction": 0.3,
            "restitution": 0.3
        },
        "ice": {
            "friction": 0.05,
            "restitution": 0.1
        },
        "rubber": {
            "friction": 0.8,
            "restitution": 0.8
        }
    }
}

# =============================================================================
# CONFIGURACIONES DE RED
# =============================================================================

# Configuración de red
NETWORK_CONFIG = {
    "max_players": 100,
    "tick_rate": 60,
    "interpolation_delay": 100,
    "max_ping": 200,
    "timeout": 30000,
    "reconnect_attempts": 3,
    "reconnect_delay": 5000
}

# Eventos de red
NETWORK_EVENTS = {
    "PLAYER_JOIN": "player:join",
    "PLAYER_LEAVE": "player:leave",
    "PLAYER_MOVE": "player:move",
    "PLAYER_ACTION": "player:action",
    "CHAT_MESSAGE": "chat:message",
    "VOICE_DATA": "voice:data",
    "SCENE_UPDATE": "scene:update",
    "ASSET_UPDATE": "asset:update"
}

# =============================================================================
# CONFIGURACIONES DE ASSETS
# =============================================================================

# Tipos de archivo soportados
SUPPORTED_FILE_TYPES = {
    "models": [".glb", ".gltf", ".obj", ".fbx", ".dae"],
    "textures": [".jpg", ".jpeg", ".png", ".webp", ".ktx2"],
    "sounds": [".mp3", ".wav", ".ogg", ".m4a"],
    "animations": [".fbx", ".dae", ".bvh"],
    "videos": [".mp4", ".webm", ".ogg"]
}

# Límites de archivo
FILE_LIMITS = {
    "max_model_size": 50 * 1024 * 1024,  # 50MB
    "max_texture_size": 10 * 1024 * 1024,  # 10MB
    "max_sound_size": 5 * 1024 * 1024,   # 5MB
    "max_animation_size": 20 * 1024 * 1024,  # 20MB
    "max_video_size": 100 * 1024 * 1024,  # 100MB
    "max_total_size": 500 * 1024 * 1024   # 500MB
}

# Configuración de optimización de assets
ASSET_OPTIMIZATION = {
    "texture_compression": "ktx2",
    "model_compression": "draco",
    "max_texture_resolution": 2048,
    "max_polygon_count": 100000,
    "enable_lod": True,
    "lod_levels": 3
}

# =============================================================================
# CONFIGURACIONES DE BLOCKCHAIN
# =============================================================================

# Configuración de contratos inteligentes
SMART_CONTRACTS = {
    "nft_contract": os.getenv("NFT_CONTRACT_ADDRESS", ""),
    "marketplace_contract": os.getenv("MARKETPLACE_CONTRACT_ADDRESS", ""),
    "governance_contract": os.getenv("GOVERNANCE_CONTRACT_ADDRESS", ""),
    "staking_contract": os.getenv("STAKING_CONTRACT_ADDRESS", "")
}

# Configuración de gas
GAS_SETTINGS = {
    "default_gas_limit": 300000,
    "default_gas_price": 20000000000,  # 20 Gwei
    "max_gas_price": 100000000000,     # 100 Gwei
    "priority_fee": 1500000000         # 1.5 Gwei
}

# Configuración de fees
FEE_SETTINGS = {
    "platform_fee": 0.025,  # 2.5%
    "creator_royalty": 0.05,  # 5%
    "min_transaction_fee": 0.001,  # 0.1%
    "max_transaction_fee": 0.10   # 10%
}

# =============================================================================
# CONFIGURACIONES DE SEGURIDAD
# =============================================================================

# Configuración de autenticación
AUTH_CONFIG = {
    "jwt_secret": os.getenv("JWT_SECRET", "your-secret-key"),
    "jwt_expiration": 24 * 60 * 60,  # 24 horas
    "refresh_token_expiration": 7 * 24 * 60 * 60,  # 7 días
    "max_login_attempts": 5,
    "lockout_duration": 15 * 60,  # 15 minutos
    "password_min_length": 8,
    "require_special_chars": True
}

# Configuración de CORS
CORS_CONFIG = {
    "allowed_origins": [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://woldvirtual.com",
        "https://app.woldvirtual.com"
    ],
    "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allowed_headers": ["Content-Type", "Authorization"],
    "allow_credentials": True
}

# Configuración de rate limiting
RATE_LIMIT_CONFIG = {
    "requests_per_minute": 100,
    "requests_per_hour": 1000,
    "requests_per_day": 10000,
    "burst_limit": 20
}

# =============================================================================
# CONFIGURACIONES DE CACHE
# =============================================================================

# Configuración de Redis
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", "6379")),
    "db": int(os.getenv("REDIS_DB", "0")),
    "password": os.getenv("REDIS_PASSWORD", None),
    "max_connections": 20,
    "connection_timeout": 5,
    "read_timeout": 10
}

# Configuración de cache
CACHE_CONFIG = {
    "default_ttl": 3600,  # 1 hora
    "session_ttl": 1800,  # 30 minutos
    "asset_ttl": 86400,   # 24 horas
    "scene_ttl": 7200,    # 2 horas
    "user_ttl": 1800      # 30 minutos
}

# =============================================================================
# CONFIGURACIONES DE LOGGING
# =============================================================================

# Configuración de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/woldvirtual.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# =============================================================================
# CONFIGURACIONES DE MONITOREO
# =============================================================================

# Configuración de métricas
METRICS_CONFIG = {
    "enabled": True,
    "collector_interval": 60,  # segundos
    "retention_days": 30,
    "alert_thresholds": {
        "cpu_usage": 80,
        "memory_usage": 85,
        "disk_usage": 90,
        "response_time": 2000,  # ms
        "error_rate": 5  # %
    }
}

# Configuración de health checks
HEALTH_CHECK_CONFIG = {
    "enabled": True,
    "interval": 30,  # segundos
    "timeout": 10,   # segundos
    "checks": [
        "database",
        "redis",
        "web3_provider",
        "ipfs_gateway",
        "external_apis"
    ]
}

# =============================================================================
# VALORES POR DEFECTO
# =============================================================================

# Valores por defecto para usuarios
DEFAULT_USER_SETTINGS = {
    "theme": "dark",
    "language": "es",
    "timezone": "UTC",
    "notifications": {
        "email": True,
        "push": True,
        "in_app": True
    },
    "privacy": {
        "profile_public": True,
        "show_earnings": False,
        "allow_messages": True
    }
}

# Valores por defecto para escenas
DEFAULT_SCENE_SETTINGS = {
    "physics_enabled": True,
    "collision_detection": True,
    "shadows_enabled": True,
    "fog_enabled": False,
    "skybox_enabled": True,
    "post_processing": True
}

# Valores por defecto para assets
DEFAULT_ASSET_SETTINGS = {
    "auto_optimize": True,
    "generate_thumbnails": True,
    "extract_metadata": True,
    "validate_format": True,
    "backup_to_ipfs": True
}

# =============================================================================
# MENSAJES DE ERROR
# =============================================================================

ERROR_MESSAGES = {
    "validation": {
        "required_field": "El campo {field} es requerido",
        "invalid_format": "El formato de {field} no es válido",
        "min_length": "El campo {field} debe tener al menos {min} caracteres",
        "max_length": "El campo {field} no puede exceder {max} caracteres",
        "invalid_email": "El email proporcionado no es válido",
        "invalid_wallet": "La dirección de wallet no es válida",
        "file_too_large": "El archivo excede el tamaño máximo permitido",
        "unsupported_format": "El formato de archivo no está soportado"
    },
    "authentication": {
        "invalid_credentials": "Credenciales inválidas",
        "account_locked": "Cuenta bloqueada temporalmente",
        "token_expired": "Token de acceso expirado",
        "insufficient_permissions": "Permisos insuficientes",
        "wallet_not_connected": "Wallet no conectada"
    },
    "blockchain": {
        "transaction_failed": "La transacción falló",
        "insufficient_balance": "Saldo insuficiente",
        "gas_limit_exceeded": "Límite de gas excedido",
        "network_error": "Error de red blockchain",
        "contract_error": "Error en el contrato inteligente"
    },
    "network": {
        "connection_failed": "Error de conexión",
        "timeout": "Tiempo de espera agotado",
        "server_error": "Error del servidor",
        "rate_limit_exceeded": "Límite de velocidad excedido"
    }
}

# =============================================================================
# CONFIGURACIONES DE DESARROLLO
# =============================================================================

# Configuración para desarrollo
if ENVIRONMENT == "development":
    DEBUG_MODE = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URL = "sqlite:///woldvirtual_dev.db"
    WEB3_PROVIDER_URL = "http://localhost:8545"
    WEB3_CHAIN_ID = 1337  # Ganache default

# Configuración para testing
if ENVIRONMENT == "testing":
    DEBUG_MODE = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URL = "sqlite:///woldvirtual_test.db"
    WEB3_PROVIDER_URL = "http://localhost:8545"
    WEB3_CHAIN_ID = 1337
    REDIS_CONFIG["db"] = 1 