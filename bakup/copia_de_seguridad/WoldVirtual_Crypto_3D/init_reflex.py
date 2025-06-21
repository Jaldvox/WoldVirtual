#!/usr/bin/env python3
"""
Script de inicialización para WoldVirtual Crypto 3D con Reflex.
Configura el entorno, instala dependencias y prepara la aplicación.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ReflexInitializer:
    """Inicializador de Reflex para WoldVirtual Crypto 3D."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_file = self.project_root / "requirements.txt"
        self.rxconfig_file = self.project_root / "rxconfig.py"
        self.state_file = self.project_root / "state.py"
        self.pages_file = self.project_root / "pages.py"
        
    def check_python_version(self):
        """Verifica la versión de Python."""
        logger.info("Verificando versión de Python...")
        
        if sys.version_info < (3, 8):
            logger.error("Se requiere Python 3.8 o superior")
            sys.exit(1)
        
        logger.info(f"Python {sys.version} detectado ✓")
    
    def check_reflex_installation(self):
        """Verifica si Reflex está instalado."""
        logger.info("Verificando instalación de Reflex...")
        
        try:
            import reflex
            logger.info(f"Reflex {reflex.__version__} detectado ✓")
            return True
        except ImportError:
            logger.warning("Reflex no está instalado")
            return False
    
    def install_dependencies(self):
        """Instala las dependencias del proyecto."""
        logger.info("Instalando dependencias...")
        
        try:
            # Actualizar pip
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True, capture_output=True)
            
            # Instalar Reflex
            subprocess.run([
                sys.executable, "-m", "pip", "install", "reflex"
            ], check=True, capture_output=True)
            
            # Instalar dependencias del proyecto
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ], check=True, capture_output=True)
            
            logger.info("Dependencias instaladas correctamente ✓")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al instalar dependencias: {e}")
            sys.exit(1)
    
    def create_env_file(self):
        """Crea el archivo .env con variables de entorno."""
        logger.info("Creando archivo .env...")
        
        env_file = self.project_root / ".env"
        
        if env_file.exists():
            logger.info("Archivo .env ya existe")
            return
        
        env_content = """# =============================================================================
# CONFIGURACIÓN DE ENTORNO - WoldVirtual Crypto 3D
# =============================================================================

# Entorno de desarrollo
ENVIRONMENT=development
DEBUG_MODE=True
LOG_LEVEL=DEBUG

# Configuración de base de datos
DATABASE_URL=sqlite:///woldvirtual.db

# Configuración de API
API_HOST=localhost
API_PORT=8000
FRONTEND_PORT=3000

# Configuración de Web3
WEB3_PROVIDER_URL=http://localhost:8545
WEB3_CHAIN_ID=1

# Configuración de IPFS
IPFS_GATEWAY=https://ipfs.io/ipfs/

# Configuración de seguridad
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-change-in-production

# Configuración de contratos inteligentes
NFT_CONTRACT_ADDRESS=
MARKETPLACE_CONTRACT_ADDRESS=
GOVERNANCE_CONTRACT_ADDRESS=
STAKING_CONTRACT_ADDRESS=

# Configuración de autenticación OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Configuración de notificaciones
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
VAPID_PUBLIC_KEY=
VAPID_PRIVATE_KEY=

# Configuración de analytics
GA_TRACKING_ID=

# Configuración de monitoreo de errores
SENTRY_DSN=

# Configuración de Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Configuración de caché
CACHE_TTL=3600
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        logger.info("Archivo .env creado ✓")
    
    def create_directories(self):
        """Crea los directorios necesarios."""
        logger.info("Creando directorios...")
        
        directories = [
            "assets",
            "assets/models",
            "assets/textures",
            "assets/sounds",
            "assets/animations",
            "assets/videos",
            "logs",
            "exports",
            "uploads",
            "temp",
            "cache",
            "docs",
            "tests",
            "tests/unit",
            "tests/integration",
            "tests/e2e",
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directorio creado: {directory}")
        
        logger.info("Directorios creados ✓")
    
    def create_gitignore(self):
        """Crea el archivo .gitignore."""
        logger.info("Creando .gitignore...")
        
        gitignore_file = self.project_root / ".gitignore"
        
        if gitignore_file.exists():
            logger.info("Archivo .gitignore ya existe")
            return
        
        gitignore_content = """# =============================================================================
# .gitignore para WoldVirtual Crypto 3D
# =============================================================================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/

# =============================================================================
# WoldVirtual Crypto 3D específico
# =============================================================================

# Reflex
.web/
export/
assets/

# Base de datos
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# Archivos temporales
temp/
cache/
uploads/

# Archivos de configuración local
config.local.py
settings.local.py

# Claves privadas
*.pem
*.key
private_key.txt

# Archivos de wallet
wallet.json
keystore/

# Archivos de IPFS
.ipfs/

# Archivos de blockchain
blockchain_data/
transactions/

# Archivos de modelos 3D (grandes)
*.glb
*.gltf
*.obj
*.fbx
*.dae

# Archivos de textura (grandes)
*.jpg
*.jpeg
*.png
*.webp
*.ktx2

# Archivos de audio (grandes)
*.mp3
*.wav
*.ogg
*.m4a

# Archivos de video (grandes)
*.mp4
*.webm
*.avi

# Archivos comprimidos
*.zip
*.rar
*.7z
*.tar.gz

# Archivos de backup
*.bak
*.backup

# Archivos de sistema
.DS_Store
Thumbs.db

# Archivos de desarrollo
.env.local
.env.development
.env.test
.env.production

# Archivos de despliegue
deploy/
production/
staging/

# Archivos de monitoreo
metrics/
analytics/

# Archivos de testing
test_results/
coverage_reports/
"""
        
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        logger.info(".gitignore creado ✓")
    
    def create_docker_files(self):
        """Crea archivos de Docker."""
        logger.info("Creando archivos de Docker...")
        
        # Dockerfile
        dockerfile_content = """# =============================================================================
# Dockerfile para WoldVirtual Crypto 3D
# =============================================================================

FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    git \\
    libpq-dev \\
    ffmpeg \\
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p assets logs exports uploads temp cache

# Exponer puertos
EXPOSE 3000 8000

# Comando por defecto
CMD ["reflex", "run", "--host", "0.0.0.0", "--port", "3000"]
"""
        
        with open(self.project_root / "Dockerfile", 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        # docker-compose.yml
        docker_compose_content = """# =============================================================================
# docker-compose.yml para WoldVirtual Crypto 3D
# =============================================================================

version: '3.8'

services:
  # Aplicación principal
  woldvirtual:
    build: .
    ports:
      - "3000:3000"
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/woldvirtual
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    volumes:
      - ./assets:/app/assets
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # Base de datos PostgreSQL
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=woldvirtual
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis para caché
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # IPFS
  ipfs:
    image: ipfs/kubo:latest
    ports:
      - "4001:4001"
      - "5001:5001"
      - "8080:8080"
    volumes:
      - ipfs_data:/data/ipfs
    restart: unless-stopped

  # Ganache para desarrollo blockchain
  ganache:
    image: trufflesuite/ganache:latest
    ports:
      - "8545:8545"
    environment:
      - GANACHE_DB=/data
      - GANACHE_NETWORK_ID=1337
      - GANACHE_DETERMINISTIC=true
    volumes:
      - ganache_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  ipfs_data:
  ganache_data:
"""
        
        with open(self.project_root / "docker-compose.yml", 'w', encoding='utf-8') as f:
            f.write(docker_compose_content)
        
        logger.info("Archivos de Docker creados ✓")
    
    def create_makefile(self):
        """Crea un Makefile para comandos útiles."""
        logger.info("Creando Makefile...")
        
        makefile_content = """# =============================================================================
# Makefile para WoldVirtual Crypto 3D
# =============================================================================

.PHONY: help install dev test build deploy clean docker-up docker-down

# Comando por defecto
help:
	@echo "Comandos disponibles:"
	@echo "  install    - Instalar dependencias"
	@echo "  dev        - Ejecutar en modo desarrollo"
	@echo "  test       - Ejecutar tests"
	@echo "  build      - Construir aplicación"
	@echo "  deploy     - Desplegar aplicación"
	@echo "  clean      - Limpiar archivos temporales"
	@echo "  docker-up  - Levantar servicios con Docker"
	@echo "  docker-down- Detener servicios de Docker"

# Instalar dependencias
install:
	pip install -r requirements.txt
	reflex init

# Ejecutar en modo desarrollo
dev:
	reflex run --host 0.0.0.0 --port 3000

# Ejecutar tests
test:
	pytest tests/ -v --cov=.

# Construir aplicación
build:
	reflex export

# Desplegar aplicación
deploy:
	reflex deploy

# Limpiar archivos temporales
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .web/
	rm -rf export/
	rm -rf logs/*.log
	rm -rf temp/*
	rm -rf cache/*

# Levantar servicios con Docker
docker-up:
	docker-compose up -d

# Detener servicios de Docker
docker-down:
	docker-compose down

# Ver logs de Docker
docker-logs:
	docker-compose logs -f

# Reconstruir y levantar Docker
docker-rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

# Backup de base de datos
backup-db:
	docker-compose exec db pg_dump -U postgres woldvirtual > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar base de datos
restore-db:
	docker-compose exec -T db psql -U postgres woldvirtual < $(FILE)

# Verificar estado de servicios
status:
	docker-compose ps
"""
        
        with open(self.project_root / "Makefile", 'w', encoding='utf-8') as f:
            f.write(makefile_content)
        
        logger.info("Makefile creado ✓")
    
    def run_reflex_init(self):
        """Ejecuta la inicialización de Reflex."""
        logger.info("Inicializando Reflex...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "reflex", "init"
            ], check=True, capture_output=True)
            
            logger.info("Reflex inicializado correctamente ✓")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al inicializar Reflex: {e}")
            sys.exit(1)
    
    def verify_setup(self):
        """Verifica que todo esté configurado correctamente."""
        logger.info("Verificando configuración...")
        
        # Verificar archivos esenciales
        essential_files = [
            "rxconfig.py",
            "state.py",
            "pages.py",
            "requirements.txt",
            ".env",
            ".gitignore"
        ]
        
        for file in essential_files:
            if (self.project_root / file).exists():
                logger.info(f"✓ {file}")
            else:
                logger.error(f"✗ {file} - FALTANTE")
        
        # Verificar directorios
        essential_dirs = [
            "assets",
            "logs",
            "utils",
            "components",
            "models"
        ]
        
        for dir in essential_dirs:
            if (self.project_root / dir).exists():
                logger.info(f"✓ directorio {dir}")
            else:
                logger.error(f"✗ directorio {dir} - FALTANTE")
        
        logger.info("Verificación completada")
    
    def run(self):
        """Ejecuta todo el proceso de inicialización."""
        logger.info("🚀 Iniciando configuración de WoldVirtual Crypto 3D con Reflex")
        
        # Verificar Python
        self.check_python_version()
        
        # Verificar Reflex
        if not self.check_reflex_installation():
            self.install_dependencies()
        
        # Crear archivos de configuración
        self.create_env_file()
        self.create_gitignore()
        self.create_directories()
        self.create_docker_files()
        self.create_makefile()
        
        # Inicializar Reflex
        self.run_reflex_init()
        
        # Verificar configuración
        self.verify_setup()
        
        logger.info("✅ Configuración completada exitosamente!")
        logger.info("")
        logger.info("📋 Próximos pasos:")
        logger.info("1. Edita el archivo .env con tus configuraciones")
        logger.info("2. Ejecuta 'make dev' para iniciar en modo desarrollo")
        logger.info("3. Visita http://localhost:3000 en tu navegador")
        logger.info("")
        logger.info("🔧 Comandos útiles:")
        logger.info("- make dev      : Ejecutar en desarrollo")
        logger.info("- make test     : Ejecutar tests")
        logger.info("- make docker-up: Levantar con Docker")
        logger.info("- make clean    : Limpiar archivos temporales")

def main():
    """Función principal."""
    initializer = ReflexInitializer()
    initializer.run()

if __name__ == "__main__":
    main() 