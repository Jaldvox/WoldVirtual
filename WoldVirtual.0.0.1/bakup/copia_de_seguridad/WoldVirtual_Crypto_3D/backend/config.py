"""Configuración del backend."""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./woldvirtual.db"
    )
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "tu_clave_secreta_aqui"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de IPFS
    IPFS_API_URL: str = os.getenv(
        "IPFS_API_URL",
        "http://localhost:5001"
    )
    
    # Configuración de Web3
    WEB3_PROVIDER_URL: str = os.getenv(
        "WEB3_PROVIDER_URL",
        "http://localhost:8545"
    )
    CONTRACT_ADDRESS: str = os.getenv(
        "CONTRACT_ADDRESS",
        "0x0000000000000000000000000000000000000000"
    )
    
    # Configuración de CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://woldvirtual.com",
    ]
    
    # Configuración de almacenamiento
    UPLOAD_FOLDER: str = "uploads"
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    
    class Config:
        """Configuración de Pydantic."""
        env_file = ".env"
        case_sensitive = True

settings = Settings() 