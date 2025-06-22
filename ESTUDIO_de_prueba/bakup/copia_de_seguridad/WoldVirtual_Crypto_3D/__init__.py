"""
WoldVirtual Crypto 3D - Sistema de visualización 3D para criptomonedas
"""

__version__ = "0.0.9"
__author__ = "WoldVirtual Team"

# Importaciones principales del proyecto
# from .core.engine import Engine3D
# from .core.security_manager import SecurityManager
# from .config.settings import Settings

# Configurar logging principal
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"WoldVirtual Crypto 3D v{__version__} initialized")