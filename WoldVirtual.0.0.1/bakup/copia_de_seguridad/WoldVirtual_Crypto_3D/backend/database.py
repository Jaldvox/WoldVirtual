"""Configuración de la base de datos."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./woldvirtual.db"
)

# Crear el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base para los modelos
Base = declarative_base()

def get_db():
    """Obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 