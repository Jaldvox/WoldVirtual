"""Configuración de Reflex para WoldVirtual Crypto 3D."""
import reflex as rx
import os
from typing import Dict, List, Any

# Configuración de entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///woldvirtual.db")

# Configuración de API
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))

# Configuración de Web3
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
WEB3_CHAIN_ID = int(os.getenv("WEB3_CHAIN_ID", "1"))

# Configuración de IPFS
IPFS_GATEWAY = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs/")

# Configuración de CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://woldvirtual.com",
    "https://app.woldvirtual.com"
]

# Configuración de caché
CACHE_CONTROL = "no-cache" if DEBUG_MODE else "public, max-age=3600"

# Configuración de Tailwind CSS
TAILWIND_CONFIG = {
    "theme": {
        "extend": {
            "colors": {
                "primary": {
                    "50": "#eff6ff",
                    "100": "#dbeafe",
                    "200": "#bfdbfe",
                    "300": "#93c5fd",
                    "400": "#60a5fa",
                    "500": "#3b82f6",
                    "600": "#2563eb",
                    "700": "#1d4ed8",
                    "800": "#1e40af",
                    "900": "#1e3a8a",
                },
                "secondary": {
                    "50": "#fdf4ff",
                    "100": "#fae8ff",
                    "200": "#f5d0fe",
                    "300": "#f0abfc",
                    "400": "#e879f9",
                    "500": "#d946ef",
                    "600": "#c026d3",
                    "700": "#a21caf",
                    "800": "#86198f",
                    "900": "#701a75",
                },
                "accent": {
                    "50": "#fff7ed",
                    "100": "#ffedd5",
                    "200": "#fed7aa",
                    "300": "#fdba74",
                    "400": "#fb923c",
                    "500": "#f97316",
                    "600": "#ea580c",
                    "700": "#c2410c",
                    "800": "#9a3412",
                    "900": "#7c2d12",
                }
            },
            "fontFamily": {
                "sans": ["Inter", "system-ui", "sans-serif"],
                "mono": ["Fira Code", "monospace"],
            },
            "animation": {
                "fade-in": "fadeIn 0.5s ease-in-out",
                "slide-up": "slideUp 0.3s ease-out",
                "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
            },
            "keyframes": {
                "fadeIn": {
                    "0%": {"opacity": "0"},
                    "100%": {"opacity": "1"},
                },
                "slideUp": {
                    "0%": {"transform": "translateY(10px)", "opacity": "0"},
                    "100%": {"transform": "translateY(0)", "opacity": "1"},
                },
            },
        }
    },
}

# Configuración principal de Reflex
config = rx.Config(
    # Configuración básica
    app_name="WoldVirtual_Crypto_3D",
    app_version="0.0.9",
    description="Metaverso descentralizado 3D con capacidades de criptomonedas",
    
    # Configuración de entorno
    env=rx.Env.DEV if ENVIRONMENT == "development" else rx.Env.PROD,
    debug=DEBUG_MODE,
    
    # Configuración de puertos
    frontend_port=FRONTEND_PORT,
    backend_port=API_PORT,
    
    # Configuración de URLs
    api_url=f"http://{API_HOST}:{API_PORT}",
    deploy_url=f"http://{API_HOST}:{FRONTEND_PORT}",
    
    # Configuración de base de datos
    db_url=DATABASE_URL,
    
    # Configuración de CORS
    cors_allowed_origins=CORS_ALLOWED_ORIGINS,
    
    # Configuración de caché
    cache_control=CACHE_CONTROL,
    
    # Configuración de Tailwind
    tailwind=TAILWIND_CONFIG,
    plugins=[rx.plugins.TailwindV3Plugin()],
    
    # Configuración de variables de entorno
    env_vars={
        "ENVIRONMENT": ENVIRONMENT,
        "DEBUG_MODE": str(DEBUG_MODE),
        "WEB3_PROVIDER_URL": WEB3_PROVIDER_URL,
        "WEB3_CHAIN_ID": str(WEB3_CHAIN_ID),
        "IPFS_GATEWAY": IPFS_GATEWAY,
        "DATABASE_URL": DATABASE_URL,
    },
    
    # Configuración de seguridad
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    
    # Configuración de logging
    log_level="DEBUG" if DEBUG_MODE else "INFO",
    
    # Configuración de compilación
    build_path=".web",
    export_path="export",
    
    # Configuración de desarrollo
    frontend_path="frontend",
    backend_path="backend",
    
    # Configuración de assets
    assets_path="assets",
    
    # Configuración de testing
    test_path="tests",
    
    # Configuración de documentación
    docs_path="docs",
    
    # Configuración de migraciones
    alembic_config="alembic.ini",
    
    # Configuración de WebSocket
    websocket_ping_interval=20,
    websocket_ping_timeout=20,
    
    # Configuración de rate limiting
    rate_limit_requests=100,
    rate_limit_window=60,
    
    # Configuración de sesiones
    session_expiry=3600,  # 1 hora
    
    # Configuración de archivos
    max_file_size=50 * 1024 * 1024,  # 50MB
    allowed_file_types=[
        ".glb", ".gltf", ".obj", ".fbx", ".dae",  # Modelos 3D
        ".jpg", ".jpeg", ".png", ".webp", ".ktx2",  # Texturas
        ".mp3", ".wav", ".ogg", ".m4a",  # Audio
        ".mp4", ".webm", ".ogg",  # Video
    ],
    
    # Configuración de optimización
    enable_compression=True,
    enable_minification=not DEBUG_MODE,
    enable_source_maps=DEBUG_MODE,
    
    # Configuración de monitoreo
    enable_metrics=True,
    enable_health_checks=True,
    
    # Configuración de caché de assets
    asset_cache_control="public, max-age=31536000",  # 1 año
    
    # Configuración de CSP (Content Security Policy)
    content_security_policy={
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
        "connect-src": ["'self'", "wss:", "https:"],
        "font-src": ["'self'", "https:"],
        "object-src": ["'none'"],
        "media-src": ["'self'", "https:"],
        "frame-src": ["'none'"],
    },
    
    # Configuración de headers de seguridad
    security_headers={
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    },
)

# Configuración específica por entorno
if ENVIRONMENT == "production":
    config.debug = False
    config.env = rx.Env.PROD
    config.cache_control = "public, max-age=3600"
    config.enable_minification = True
    config.enable_source_maps = False
    config.log_level = "WARNING"
    
elif ENVIRONMENT == "staging":
    config.debug = False
    config.env = rx.Env.STAGING
    config.cache_control = "public, max-age=1800"
    config.enable_minification = True
    config.enable_source_maps = True
    config.log_level = "INFO"

# Configuración de desarrollo
if DEBUG_MODE:
    config.cors_allowed_origins.extend([
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
    ]) 