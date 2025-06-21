"""
Módulo de páginas de Wold Virtual 3D
Contiene todas las páginas de la aplicación
"""

# Páginas principales
from .home import HomePage
from .about import AboutPage
from .three_d_scene import ThreeDScenePage

# Páginas de autenticación
from .auth import LoginPage, RegisterPage

# Páginas de configuración
from .settings import SettingsPage

# Páginas de dashboard
from .dashboard import DashboardPage

__all__ = [
    # Páginas principales
    'HomePage',
    'AboutPage', 
    'ThreeDScenePage',
    
    # Autenticación
    'LoginPage',
    'RegisterPage',
    
    # Configuración
    'SettingsPage',
    
    # Dashboard
    'DashboardPage'
]