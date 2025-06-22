"""
WoldVirtual Crypto 3D - Configuración Principal de Reflex
========================================================

Este archivo contiene toda la configuración necesaria para el ecosistema
WoldVirtual Crypto 3D, incluyendo configuraciones de desarrollo, producción,
base de datos, Web3, seguridad y optimizaciones.

Autor: WoldVirtual Team
Versión: 0.0.9
Fecha: Junio 2025
"""

import reflex as rx
import os
from typing import Dict, List, Any, Optional

# ============================================================================
# CONFIGURACIÓN DE ENTORNO Y VARIABLES GLOBALES
# ============================================================================

class EnvironmentConfig:
    """Gestión centralizada de variables de entorno y configuración del sistema."""
    
    # Configuración básica del entorno
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
    VERSION = "0.0.9"
    APP_NAME = "WoldVirtual_Crypto_3D"
    
    # Configuración de red y puertos
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))
    
    # Configuración de base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///woldvirtual_crypto_3d.db")
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "woldvirtual-dev-key-change-in-production")
    
    # Configuración de Web3 y Blockchain
    WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
    WEB3_CHAIN_ID = int(os.getenv("WEB3_CHAIN_ID", "1"))  # Ethereum Mainnet
    WEB3_FALLBACK_PROVIDER = os.getenv("WEB3_FALLBACK_PROVIDER", "https://cloudflare-eth.com")
    
    # Configuración de IPFS para almacenamiento descentralizado
    IPFS_GATEWAY = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs/")
    IPFS_API_URL = os.getenv("IPFS_API_URL", "http://localhost:5001")
    
    # Configuración de servicios externos
    PINATA_API_KEY = os.getenv("PINATA_API_KEY", "")  # Para IPFS pinning
    PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY", "")

# ============================================================================
# CONFIGURACIÓN DE CORS Y SEGURIDAD
# ============================================================================

class SecurityConfig:
    """Configuración de seguridad, CORS y políticas de contenido."""
    
    @staticmethod
    def get_cors_origins() -> List[str]:
        """
        Retorna las URLs permitidas para CORS según el entorno.
        
        Returns:
            List[str]: Lista de orígenes permitidos para CORS
        """
        base_origins = [
            # Desarrollo local
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000",
            # React frontend
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
        
        if EnvironmentConfig.ENVIRONMENT == "production":
            base_origins.extend([
                "https://woldvirtual.com",
                "https://app.woldvirtual.com",
                "https://metaverse.woldvirtual.com",
            ])
        elif EnvironmentConfig.ENVIRONMENT == "staging":
            base_origins.extend([
                "https://staging.woldvirtual.com",
                "https://test.woldvirtual.com",
            ])
        
        return base_origins
    
    @staticmethod
    def get_content_security_policy() -> Dict[str, List[str]]:
        """
        Configuración de Content Security Policy para seguridad web.
        
        Returns:
            Dict[str, List[str]]: Políticas de seguridad de contenido
        """
        return {
            "default-src": ["'self'"],
            "script-src": [
                "'self'", 
                "'unsafe-inline'",  # Necesario para Three.js
                "'unsafe-eval'",    # Necesario para algunos frameworks
                "https://cdn.ethers.io",  # Web3 libraries
            ],
            "style-src": [
                "'self'", 
                "'unsafe-inline'",  # Necesario para Tailwind CSS
                "https://fonts.googleapis.com",
            ],
            "img-src": [
                "'self'", 
                "data:", 
                "https:",
                "https://ipfs.io",  # IPFS images
                "https://gateway.pinata.cloud",  # Pinata IPFS
            ],
            "connect-src": [
                "'self'", 
                "wss:", 
                "https:",
                "https://cloudflare-eth.com",  # Ethereum provider
            ],
            "font-src": [
                "'self'", 
                "https://fonts.gstatic.com",
            ],
            "object-src": ["'none'"],
            "media-src": ["'self'", "https:", "blob:"],  # Para audio/video 3D
            "frame-src": ["'none'"],
            "worker-src": ["'self'", "blob:"],  # Para Web Workers en Three.js
        }
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """
        Headers de seguridad adicionales.
        
        Returns:
            Dict[str, str]: Headers de seguridad HTTP
        """
        return {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }

# ============================================================================
# CONFIGURACIÓN DE TAILWIND CSS Y ESTILOS
# ============================================================================

class TailwindConfig:
    """Configuración personalizada de Tailwind CSS para WoldVirtual."""
    
    @staticmethod
    def get_tailwind_config() -> Dict[str, Any]:
        """
        Configuración completa de Tailwind CSS con tema personalizado.
        
        Returns:
            Dict[str, Any]: Configuración de Tailwind CSS
        """
        return {
            "theme": {
                "extend": {
                    # Paleta de colores del metaverso
                    "colors": {
                        # Verde neón principal (identidad WoldVirtual)
                        "primary": {
                            "50": "#f0fdf0",
                            "100": "#dcfce7",
                            "200": "#bbf7d0",
                            "300": "#86efac",
                            "400": "#4ade80",
                            "500": "#00ff00",  # Verde neón principal
                            "600": "#00e600",
                            "700": "#00cc00",
                            "800": "#009900",
                            "900": "#006600",
                        },
                        # Azul cibernético secundario
                        "secondary": {
                            "50": "#eff6ff",
                            "100": "#dbeafe",
                            "200": "#bfdbfe",
                            "300": "#93c5fd",
                            "400": "#60a5fa",
                            "500": "#0099ff",  # Azul principal
                            "600": "#0080ff",
                            "700": "#0066cc",
                            "800": "#004d99",
                            "900": "#003366",
                        },
                        # Naranja de acento
                        "accent": {
                            "50": "#fff7ed",
                            "100": "#ffedd5",
                            "200": "#fed7aa",
                            "300": "#fdba74",
                            "400": "#fb923c",
                            "500": "#ff6b35",  # Naranja principal
                            "600": "#e6522a",
                            "700": "#cc3d1f",
                            "800": "#b32814",
                            "900": "#99140a",
                        },
                        # Tonos oscuros para el metaverso
                        "dark": {
                            "50": "#f8fafc",
                            "100": "#f1f5f9",
                            "200": "#e2e8f0",
                            "300": "#cbd5e1",
                            "400": "#94a3b8",
                            "500": "#64748b",
                            "600": "#475569",
                            "700": "#334155",
                            "800": "#1e293b",
                            "900": "#0f172a",
                            "950": "#020617",
                        },
                        # Colores específicos del metaverso
                        "metaverse": {
                            "bg-primary": "#1a1a2e",
                            "bg-secondary": "#16213e",
                            "bg-tertiary": "#0f0f23",
                            "text-primary": "#ffffff",
                            "text-secondary": "#cccccc",
                            "text-muted": "#888888",
                            "border": "#333333",
                        }
                    },
                    
                    # Tipografía especializada
                    "fontFamily": {
                        "sans": ["Inter", "system-ui", "sans-serif"],
                        "mono": ["Fira Code", "JetBrains Mono", "monospace"],
                        "display": ["Orbitron", "Inter", "sans-serif"],  # Para títulos futuristas
                    },
                    
                    # Animaciones para el metaverso
                    "animation": {
                        "fade-in": "fadeIn 0.5s ease-in-out",
                        "fade-out": "fadeOut 0.5s ease-in-out",
                        "slide-up": "slideUp 0.3s ease-out",
                        "slide-down": "slideDown 0.3s ease-out",
                        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
                        "glow": "glow 2s ease-in-out infinite alternate",
                        "float": "float 6s ease-in-out infinite",
                        "rotate-slow": "rotate 20s linear infinite",
                        "matrix-rain": "matrixRain 20s linear infinite",
                    },
                    
                    # Keyframes personalizados
                    "keyframes": {
                        "fadeIn": {
                            "0%": {"opacity": "0"},
                            "100%": {"opacity": "1"},
                        },
                        "fadeOut": {
                            "0%": {"opacity": "1"},
                            "100%": {"opacity": "0"},
                        },
                        "slideUp": {
                            "0%": {"transform": "translateY(10px)", "opacity": "0"},
                            "100%": {"transform": "translateY(0)", "opacity": "1"},
                        },
                        "slideDown": {
                            "0%": {"transform": "translateY(-10px)", "opacity": "0"},
                            "100%": {"transform": "translateY(0)", "opacity": "1"},
                        },
                        "glow": {
                            "0%": {"box-shadow": "0 0 5px rgba(0, 255, 0, 0.5)"},
                            "100%": {"box-shadow": "0 0 20px rgba(0, 255, 0, 0.8)"},
                        },
                        "float": {
                            "0%, 100%": {"transform": "translateY(0px)"},
                            "50%": {"transform": "translateY(-20px)"},
                        },
                        "matrixRain": {
                            "0%": {"transform": "translateY(-100vh)"},
                            "100%": {"transform": "translateY(100vh)"},
                        },
                    },
                    
                    # Espaciado personalizado
                    "spacing": {
                        "72": "18rem",
                        "84": "21rem",
                        "96": "24rem",
                    },
                    
                    # Sombras especiales para efectos 3D
                    "boxShadow": {
                        "glow-sm": "0 0 10px rgba(0, 255, 0, 0.3)",
                        "glow": "0 0 20px rgba(0, 255, 0, 0.5)",
                        "glow-lg": "0 0 30px rgba(0, 255, 0, 0.7)",
                        "inner-glow": "inset 0 0 10px rgba(0, 255, 0, 0.3)",
                        "metaverse": "0 25px 50px -12px rgba(0, 0, 0, 0.8)",
                    },
                    
                    # Gradientes para efectos futuristas
                    "backgroundImage": {
                        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
                        "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
                        "metaverse-gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
                        "neon-gradient": "linear-gradient(45deg, #00ff00, #0099ff)",
                    },
                }
            },
            
            # Plugins adicionales de Tailwind
            "plugins": [
                # Plugin para animaciones más avanzadas (si se instala)
                # "@tailwindcss/animations",
            ],
        }

# ============================================================================
# CONFIGURACIÓN DE ARCHIVOS Y ASSETS
# ============================================================================

class AssetsConfig:
    """Configuración para manejo de archivos y assets del metaverso."""
    
    # Tamaños máximos de archivos (en bytes)
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB para modelos 3D grandes
    MAX_TEXTURE_SIZE = 50 * 1024 * 1024  # 50MB para texturas 4K
    MAX_AUDIO_SIZE = 25 * 1024 * 1024   # 25MB para audio de alta calidad
    
    # Tipos de archivos permitidos por categoría
    ALLOWED_3D_MODELS = [".glb", ".gltf", ".obj", ".fbx", ".dae", ".3ds", ".ply"]
    ALLOWED_TEXTURES = [".jpg", ".jpeg", ".png", ".webp", ".ktx2", ".dds", ".hdr", ".exr"]
    ALLOWED_AUDIO = [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"]
    ALLOWED_VIDEO = [".mp4", ".webm", ".ogg", ".mov", ".avi"]
    ALLOWED_DOCUMENTS = [".pdf", ".txt", ".md", ".json", ".xml"]
    
    @classmethod
    def get_all_allowed_types(cls) -> List[str]:
        """
        Retorna todos los tipos de archivos permitidos.
        
        Returns:
            List[str]: Lista completa de extensiones permitidas
        """
        return (
            cls.ALLOWED_3D_MODELS + 
            cls.ALLOWED_TEXTURES + 
            cls.ALLOWED_AUDIO + 
            cls.ALLOWED_VIDEO + 
            cls.ALLOWED_DOCUMENTS
        )

# ============================================================================
# CONFIGURACIÓN PRINCIPAL DE REFLEX
# ============================================================================

def create_reflex_config() -> rx.Config:
    """
    Crea y retorna la configuración principal de Reflex.
    
    Esta función centraliza toda la configuración de la aplicación,
    aplicando diferentes ajustes según el entorno (desarrollo/producción).
    
    Returns:
        rx.Config: Objeto de configuración de Reflex completamente configurado
    """
    
    # Determinar configuraciones según el entorno
    cache_control = "no-cache" if EnvironmentConfig.DEBUG_MODE else "public, max-age=3600"
    log_level = "DEBUG" if EnvironmentConfig.DEBUG_MODE else "INFO"
    
    # Configuración base
    base_config = {
        # ===== INFORMACIÓN BÁSICA DE LA APLICACIÓN =====
        "app_name": EnvironmentConfig.APP_NAME,
        "app_version": EnvironmentConfig.VERSION,
        "description": "Metaverso descentralizado 3D con capacidades de criptomonedas y NFTs",
        
        # ===== CONFIGURACIÓN DE ENTORNO =====
        "env": rx.Env.DEV if EnvironmentConfig.ENVIRONMENT == "development" else rx.Env.PROD,
        "debug": EnvironmentConfig.DEBUG_MODE,
        
        # ===== CONFIGURACIÓN DE RED =====
        "frontend_port": EnvironmentConfig.FRONTEND_PORT,
        "backend_port": EnvironmentConfig.API_PORT,
        "api_url": f"http://{EnvironmentConfig.API_HOST}:{EnvironmentConfig.API_PORT}",
        "deploy_url": f"http://{EnvironmentConfig.API_HOST}:{EnvironmentConfig.FRONTEND_PORT}",
        
        # ===== CONFIGURACIÓN DE BASE DE DATOS =====
        "db_url": EnvironmentConfig.DATABASE_URL,
        
        # ===== CONFIGURACIÓN DE SEGURIDAD =====
        "cors_allowed_origins": SecurityConfig.get_cors_origins(),
        "secret_key": EnvironmentConfig.SECRET_KEY,
        "content_security_policy": SecurityConfig.get_content_security_policy(),
        "security_headers": SecurityConfig.get_security_headers(),
        
        # ===== CONFIGURACIÓN DE ESTILOS =====
        "tailwind": TailwindConfig.get_tailwind_config(),
        "plugins": [rx.plugins.TailwindV3Plugin()],
        
        # ===== CONFIGURACIÓN DE CACHÉ Y OPTIMIZACIÓN =====
        "cache_control": cache_control,
        "enable_compression": True,
        "enable_minification": not EnvironmentConfig.DEBUG_MODE,
        "enable_source_maps": EnvironmentConfig.DEBUG_MODE,
        
        # ===== CONFIGURACIÓN DE LOGGING =====
        "log_level": log_level,
        
        # ===== CONFIGURACIÓN DE ARCHIVOS =====
        "max_file_size": AssetsConfig.MAX_FILE_SIZE,
        "allowed_file_types": AssetsConfig.get_all_allowed_types(),
        "assets_path": "assets",
        
        # ===== CONFIGURACIÓN DE RUTAS DE COMPILACIÓN =====
        "build_path": ".web",
        "export_path": "export",
        "frontend_path": "frontend",
        "backend_path": "backend",
        
        # ===== CONFIGURACIÓN DE WEBSOCKETS =====
        "websocket_ping_interval": 20,
        "websocket_ping_timeout": 20,
        
        # ===== CONFIGURACIÓN DE RATE LIMITING =====
        "rate_limit_requests": 100,
        "rate_limit_window": 60,
        
        # ===== CONFIGURACIÓN DE SESIONES =====
        "session_expiry": 3600,  # 1 hora
        
        # ===== CONFIGURACIÓN DE MONITOREO =====
        "enable_metrics": True,
        "enable_health_checks": True,
        
        # ===== CONFIGURACIÓN DE CACHÉ DE ASSETS =====
        "asset_cache_control": "public, max-age=31536000",  # 1 año para assets estáticos
        
        # ===== VARIABLES DE ENTORNO EXPUESTAS =====
        "env_vars": {
            "ENVIRONMENT": EnvironmentConfig.ENVIRONMENT,
            "DEBUG_MODE": str(EnvironmentConfig.DEBUG_MODE),
            "VERSION": EnvironmentConfig.VERSION,
            "WEB3_PROVIDER_URL": EnvironmentConfig.WEB3_PROVIDER_URL,
            "WEB3_CHAIN_ID": str(EnvironmentConfig.WEB3_CHAIN_ID),
            "IPFS_GATEWAY": EnvironmentConfig.IPFS_GATEWAY,
        },
    }
    
    # Crear configuración de Reflex
    config = rx.Config(**base_config)
    
    # Aplicar configuraciones específicas por entorno
    _apply_environment_specific_config(config)
    
    return config

def _apply_environment_specific_config(config: rx.Config) -> None:
    """
    Aplica configuraciones específicas según el entorno.
    
    Args:
        config (rx.Config): Objeto de configuración a modificar
    """
    if EnvironmentConfig.ENVIRONMENT == "production":
        # Configuración de producción - máxima seguridad y rendimiento
        config.debug = False
        config.env = rx.Env.PROD
        config.cache_control = "public, max-age=7200"  # 2 horas
        config.enable_minification = True
        config.enable_source_maps = False
        config.log_level = "WARNING"
        config.rate_limit_requests = 50  # Más restrictivo en producción
        
    elif EnvironmentConfig.ENVIRONMENT == "staging":
        # Configuración de staging - balance entre desarrollo y producción
        config.debug = False
        config.env = rx.Env.STAGING
        config.cache_control = "public, max-age=1800"  # 30 minutos
        config.enable_minification = True
        config.enable_source_maps = True
        config.log_level = "INFO"
        config.rate_limit_requests = 75
        
    else:  # development
        # Configuración de desarrollo - máxima facilidad de debug
        config.debug = True
        config.env = rx.Env.DEV
        config.cache_control = "no-cache"
        config.enable_minification = False
        config.enable_source_maps = True
        config.log_level = "DEBUG"
        config.rate_limit_requests = 200  # Más permisivo en desarrollo

# ============================================================================
# CONFIGURACIÓN FINAL Y EXPORTACIÓN
# ============================================================================

# Crear la configuración principal
config = create_reflex_config()

# Logging de configuración (solo en desarrollo)
if EnvironmentConfig.DEBUG_MODE:
    print(f"🚀 WoldVirtual Crypto 3D v{EnvironmentConfig.VERSION}")
    print(f"🌍 Entorno: {EnvironmentConfig.ENVIRONMENT}")
    print(f"🔧 Debug: {EnvironmentConfig.DEBUG_MODE}")
    print(f"🌐 Frontend: http://{EnvironmentConfig.API_HOST}:{EnvironmentConfig.FRONTEND_PORT}")
    print(f"⚙️  Backend: http://{EnvironmentConfig.API_HOST}:{EnvironmentConfig.API_PORT}")
    print(f"💾 Database: {EnvironmentConfig.DATABASE_URL}")
    print(f"⛓️  Web3: {EnvironmentConfig.WEB3_PROVIDER_URL} (Chain ID: {EnvironmentConfig.WEB3_CHAIN_ID})")
    print("=" * 60)