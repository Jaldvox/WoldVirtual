"""
WoldVirtual Crypto 3D - Configuración Principal de Reflex

Configuración centralizada para el ecosistema WoldVirtual Crypto 3D.
Incluye variables de entorno, puertos, base de datos, CORS y Tailwind.
"""

import reflex as rx
import os
from typing import Dict, List, Any

# =========================
# Configuración de entorno
# =========================

class EnvironmentConfig:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
    VERSION = "0.0.9"
    APP_NAME = "WoldVirtual_Crypto_3D"
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///woldvirtual_crypto_3d.db")

# =========================
# Configuración de CORS
# =========================

def get_cors_origins() -> List[str]:
    origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    if EnvironmentConfig.ENVIRONMENT == "production":
        origins += [
            "https://woldvirtual.com",
            "https://app.woldvirtual.com",
            "https://metaverse.woldvirtual.com",
        ]
    return origins

# =========================
# Configuración de Tailwind
# =========================

def get_tailwind_config() -> Dict[str, Any]:
    return {
        "theme": {
            "extend": {
                "colors": {
                    "primary": "#00ff00",
                    "secondary": "#0099ff",
                    "accent": "#ff6b35",
                    "dark": "#1a1a2e",
                    "darker": "#16213e",
                }
            }
        }
    }

# =========================
# Configuración principal Reflex
# =========================

config = rx.Config(
    app_name=EnvironmentConfig.APP_NAME,
    env=rx.Env.DEV if EnvironmentConfig.ENVIRONMENT == "development" else rx.Env.PROD,
    frontend_port=EnvironmentConfig.FRONTEND_PORT,
    backend_port=EnvironmentConfig.API_PORT,
    db_url=EnvironmentConfig.DATABASE_URL,
    cors_allowed_origins=get_cors_origins(),
    tailwind=get_tailwind_config(),
)