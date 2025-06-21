"""
Archivo principal de WoldVirtual Crypto 3D
Punto de entrada único - Botón de encendido para toda la aplicación
"""

import sys
import os
import logging
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importaciones necesarias para el funcionamiento
try:
    import reflex as rx
    from rxconfig import config
    from state import WoldVirtualState
    
    # Importar managers de assets
    from assets.asset_manager import AssetManager
    from assets.scene_manager import SceneManager
    from assets.texture_manager import TextureManager
    from assets.audio_manager import AudioManager
    print(f"✅ AssetManager imported: {AssetManager}")
    print(f"✅ SceneManager imported: {SceneManager}")
    print(f"✅ TextureManager imported: {TextureManager}")
    print(f"✅ AudioManager imported: {AudioManager}")
    
    # Importar utilidades Web3
    from utils.web3_utils import Web3Manager, WalletManager, TransactionManager
    print(f"✅ Web3Manager imported: {Web3Manager}")
except ImportError as e:
    print(f"⚠️ No se pudo importar Web3Manager: {e}")
    # Definir clases dummy para evitar errores
    class Web3Manager: 
        def __init__(self, provider_url: str = "", chain_id: int = 1):
            self.provider_url = provider_url
            self.chain_id = chain_id
    class WalletManager: 
        def __init__(self, web3_manager):
            self.web3_manager = web3_manager
    class TransactionManager: 
        def __init__(self, web3_manager):
            self.web3_manager = web3_manager
    class Database: pass
    class MainPage: pass
    class ScenePage: pass
    class SettingsPage: pass
    class HelpPage: pass
    class WoldVirtualState: pass

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('woldvirtual.log')
    ]
)

logger = logging.getLogger(__name__)

# Importaciones del proyecto
def import_modules():
    """Importar todos los módulos necesarios."""
    try:
        # Importar Reflex y configuración
        import reflex as rx
        from rxconfig import config
        
        # Importar estado
        from state import WoldVirtualState
        
        # Importar páginas
        from pages import home, explore, create, marketplace, profile, scene
        
        # Importar componentes
        from components import navbar, toolbar, scene3d, ui, profile
        
        # Importar modelos
        from models import user, asset, scene as scene_model, transaction
        
        # Importar utilidades
        from utils import constants, helpers, web3_utils, three_utils
        
        # Importar gestores de assets
        from assets import (
            asset_manager, model_manager, texture_manager, 
            audio_manager, material_manager, shader_manager,
            animation_manager, effect_manager, prefab_manager
        )
        
        # Importar backend
        from backend import database, crud, schemas, blockchain
        
        logger.info("✅ Todos los módulos importados correctamente")
        return True
        
    except ImportError as e:
        import traceback
        logger.error(f"❌ Error importing modules: {e}")
        print("\n--- TRACEBACK ---")
        traceback.print_exc()
        print("--- FIN TRACEBACK ---\n")
        logger.error("Please ensure all required modules are installed and the project structure is correct.")
        return False
    except Exception as e:
        import traceback
        logger.error(f"❌ Error importing modules: {e}")
        print("\n--- TRACEBACK ---")
        traceback.print_exc()
        print("--- FIN TRACEBACK ---\n")
        logger.error("Please ensure all required modules are installed and the project structure is correct.")
        return False

class WoldVirtualCrypto3D:
    """Clase principal de la aplicación - Botón de encendido"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.app = None
        self.web3_manager = None
        self.wallet_manager = None
        self.transaction_manager = None
        self.asset_manager = None
        self.scene_manager = None
        self.database = None
        self.is_initialized = False
        
        self.logger.info("🚀 WoldVirtual Crypto 3D - Botón de encendido inicializado")
        
    def _setup_logging(self) -> logging.Logger:
        """Configurar logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/woldvirtual.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _check_dependencies(self) -> bool:
        """Verificar que todas las dependencias estén instaladas"""
        print("🔍 Verificando dependencias...")
        
        required_packages = [
            'reflex', 'web3', 'numpy', 'PIL', 'fastapi', 
            'sqlalchemy', 'pydantic', 'uvicorn'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                print(f"  📦 Checking {package}...")
                __import__(package)
                print(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package} - FALTANTE")
        
        if missing_packages:
            print(f"❌ Dependencias faltantes: {missing_packages}")
            print("💡 Ejecuta: pip install -r requirements.txt")
            return False
        
        print("✅ Todas las dependencias verificadas")
        return True
    
    def _initialize_database(self) -> bool:
        """Inicializar base de datos"""
        try:
            print("🗄️ Inicializando base de datos...")
            print("  📋 Importing database configuration...")
            
            # Importar configuración de base de datos
            from backend.database import engine, Base
            
            print("  📋 Creating tables...")
            # Crear todas las tablas
            Base.metadata.create_all(bind=engine)
            
            print("✅ Base de datos inicializada")
            return True
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _initialize_web3(self) -> bool:
        """Inicializar componentes Web3"""
        try:
            print("🔗 Inicializando Web3...")
            
            print("  📋 Creating Web3Manager...")
            # Inicializar Web3 Manager
            provider_url = config.env_vars.get("WEB3_PROVIDER_URL", "http://localhost:8545")
            chain_id = int(config.env_vars.get("WEB3_CHAIN_ID", "1"))
            
            self.web3_manager = Web3Manager(
                provider_url=provider_url,
                chain_id=chain_id
            )
            
            print("  📋 Creating WalletManager...")
            # Inicializar Wallet Manager
            self.wallet_manager = WalletManager(self.web3_manager)
            
            print("  📋 Creating TransactionManager...")
            # Inicializar Transaction Manager
            self.transaction_manager = TransactionManager(self.web3_manager)
            
            print("✅ Web3 inicializado")
            return True
        except Exception as e:
            print(f"❌ Error inicializando Web3: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _initialize_assets(self) -> bool:
        """Inicializar gestores de assets"""
        try:
            print("🎨 Inicializando gestores de assets...")
            
            print("  📋 Creating AssetManager...")
            # Inicializar Asset Manager
            self.asset_manager = AssetManager()
            
            print("  📋 Creating SceneManager...")
            # Inicializar Scene Manager
            self.scene_manager = SceneManager()
            
            print("  📋 Creating TextureManager...")
            # Inicializar Texture Manager
            self.texture_manager = TextureManager()
            
            print("  📋 Creating AudioManager...")
            # Inicializar Audio Manager
            self.audio_manager = AudioManager()
            
            print("✅ Gestores de assets inicializados")
            return True
        except Exception as e:
            print(f"❌ Error inicializando assets: {e}")
            print("⚠️ Continuando con assets dummy...")
            # Crear instancias dummy para continuar
            self.asset_manager = type('AssetManager', (), {})()
            self.scene_manager = type('SceneManager', (), {})()
            self.texture_manager = type('TextureManager', (), {})()
            self.audio_manager = type('AudioManager', (), {})()
            print("✅ Assets dummy creados")
            return True
    
    def _create_reflex_app(self) -> bool:
        """Crear y configurar la aplicación Reflex"""
        try:
            print("🌐 Creando aplicación Reflex...")
            
            print("  📋 Importing Reflex...")
            import reflex as rx
            
            print("  📋 Creating Reflex app...")
            # Crear aplicación Reflex
            self.app = rx.App(
                _state=WoldVirtualState,
                theme=rx.theme(
                    appearance="light",
                    has_background=True,
                    radius="medium",
                    accent_color="violet",
                    gray_color="slate",
                    styles={
                        "*": {
                            "margin": "0",
                            "padding": "0",
                            "boxSizing": "border-box",
                        },
                        "html, body": {
                            "height": "100%",
                            "width": "100%",
                            "overflow": "hidden",
                            "fontFamily": "system-ui, -apple-system, sans-serif",
                        },
                        "body": {
                            "&::-webkit-scrollbar": {
                                "display": "none",
                            },
                            "scrollbarWidth": "none",
                            "msOverflowStyle": "none",
                        },
                    },
                ),
            )
            
            print("  📋 Adding pages...")
            # Agregar páginas básicas
            try:
                self.app.add_page(
                    MainPage,
                    route="/",
                    title="WoldVirtual Crypto 3D",
                    description="Metaverso descentralizado 3D con capacidades de criptomonedas",
                )
                
                self.app.add_page(
                    ScenePage,
                    route="/scene",
                    title="Escena 3D - WoldVirtual",
                )
                
                self.app.add_page(
                    SettingsPage,
                    route="/settings",
                    title="Configuración - WoldVirtual",
                )
                
                self.app.add_page(
                    HelpPage,
                    route="/help",
                    title="Ayuda - WoldVirtual",
                )
                print("  ✅ Pages added successfully")
            except Exception as e:
                print(f"  ⚠️ Warning: Could not add pages: {e}")
                print("  📋 Continuing without pages...")
            
            print("✅ Aplicación Reflex creada")
            return True
        except Exception as e:
            print(f"❌ Error creando aplicación Reflex: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _initialize_all_modules(self) -> bool:
        """Inicializar todos los módulos del sistema"""
        print("🔧 Inicializando todos los módulos...")
        
        try:
            print("  📋 Checking dependencies...")
            # Verificar dependencias
            if not self._check_dependencies():
                print("  ❌ Dependencies check failed")
                return False
            
            print("  📋 Initializing database...")
            # Inicializar base de datos
            if not self._initialize_database():
                print("  ❌ Database initialization failed")
                return False
            
            print("  📋 Initializing Web3...")
            # Inicializar Web3
            if not self._initialize_web3():
                print("  ❌ Web3 initialization failed")
                return False
            
            print("  📋 Initializing assets...")
            # Inicializar assets
            if not self._initialize_assets():
                print("  ❌ Assets initialization failed")
                return False
            
            print("  📋 Creating Reflex app...")
            # Crear aplicación Reflex
            if not self._create_reflex_app():
                print("  ❌ Reflex app creation failed")
                return False
            
            self.is_initialized = True
            print("✅ Todos los módulos inicializados correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error in _initialize_all_modules: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _start_reflex_server(self):
        """Iniciar servidor Reflex en un hilo separado"""
        try:
            self.logger.info("🚀 Iniciando servidor Reflex...")
            
            # Configurar variables de entorno para Reflex
            os.environ["REFLEX_FRONTEND_PORT"] = str(config.frontend_port)
            os.environ["REFLEX_BACKEND_PORT"] = str(config.backend_port)
            os.environ["REFLEX_API_URL"] = config.api_url
            os.environ["REFLEX_DEPLOY_URL"] = config.deploy_url
            
            # Compilar la aplicación
            self.app.compile()
            
            # Iniciar servidor
            self.app.run(
                host="0.0.0.0",
                port=config.frontend_port,
                log_level="info"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error iniciando servidor Reflex: {e}")
    
    def _show_startup_banner(self):
        """Mostrar banner de inicio"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗    ██╗ ██████╗ ██╗     ██╗     ██╗   ██╗██╗   ██╗██████╗ ██╗   ██╗    ║
║  ██║    ██║██╔═══██╗██║     ██║     ██║   ██║██║   ██║██╔══██╗██║   ██║    ║
║  ██║ █╗ ██║██║   ██║██║     ██║     ██║   ██║██║   ██║██████╔╝██║   ██║    ║
║  ██║███╗██║██║   ██║██║     ██║     ██║   ██║██║   ██║██╔══██╗██║   ██║    ║
║  ╚███╔███╔╝╚██████╔╝███████╗███████╗╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝    ║
║   ╚══╝╚══╝  ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝     ║
║                                                                              ║
║                    🚀 CRYPTO METAVERSE 3D 🚀                                ║
║                                                                              ║
║  Version: 0.0.9                    Status: Initializing...                  ║
║  Environment: Development          Framework: Reflex + Three.js             ║
║  Blockchain: Multi-chain          Database: SQLite/PostgreSQL              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def _show_system_status(self):
        """Mostrar estado del sistema"""
        status = {
            "Database": "✅ Connected" if self.database else "❌ Disconnected",
            "Web3": "✅ Connected" if self.web3_manager else "❌ Disconnected",
            "Assets": "✅ Loaded" if self.asset_manager else "❌ Not Loaded",
            "Reflex": "✅ Ready" if self.app else "❌ Not Ready",
            "Network": getattr(self.web3_manager, 'network_name', 'Unknown') if self.web3_manager else "Unknown",
            "Port": f"{config.frontend_port}",
            "Environment": config.env.value
        }
        
        print("\n📊 SYSTEM STATUS:")
        print("=" * 50)
        for key, value in status.items():
            print(f"  {key:<12}: {value}")
        print("=" * 50)
    
    def _show_access_info(self):
        """Mostrar información de acceso"""
        print("\n🌐 ACCESS INFORMATION:")
        print("=" * 50)
        print(f"  Frontend: http://localhost:{config.frontend_port}")
        print(f"  Backend:  http://localhost:{config.backend_port}")
        print(f"  API:      {config.api_url}")
        print("=" * 50)
        print("\n🎮 Ready to explore the metaverse!")
        print("   Press Ctrl+C to stop the server")
        print("=" * 50)
    
    def start(self):
        """Iniciar la aplicación completa"""
        try:
            print("🔌 Starting WoldVirtual Crypto 3D - Power Button...")
            
            # Mostrar banner
            self._show_startup_banner()
            
            print("📋 Step 1: Initializing all modules...")
            # Inicializar todos los módulos
            if not self._initialize_all_modules():
                print("❌ Failed to initialize modules")
                self.cleanup()
                return False
            
            print("📋 Step 2: Starting Reflex server...")
            # Iniciar servidor Reflex en un hilo separado
            self.server_thread = threading.Thread(
                target=self._start_reflex_server,
                daemon=True
            )
            self.server_thread.start()
            
            print("📋 Step 3: Showing system status...")
            # Mostrar estado del sistema
            self._show_system_status()
            
            print("📋 Step 4: Showing access information...")
            # Mostrar información de acceso
            self._show_access_info()
            
            print("🎮 WoldVirtual Crypto 3D is now running!")
            print("🌐 Open your browser and go to: http://localhost:3000")
            print("⏹️  Press Ctrl+C to stop the server")
            
            # Mantener la aplicación corriendo
            try:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
                print("\n🛑 Shutting down WoldVirtual Crypto 3D...")
                self.cleanup()
                return True
                
        except Exception as e:
            print(f"❌ Error in start: {e}")
            import traceback
            traceback.print_exc()
            self.cleanup()
            return False
    
    def cleanup(self):
        """Limpieza al cerrar la aplicación"""
        self.logger.info("🧹 Cleaning up resources...")
        
        try:
            # Cerrar conexiones de base de datos
            if self.database:
                self.database.close()
            
            # Cerrar conexiones Web3
            if self.web3_manager:
                self.web3_manager.w3.provider.disconnect()
            
            # Limpiar assets
            if self.asset_manager:
                self.asset_manager.cleanup()
        
            self.logger.info("✅ Cleanup completed")
            
        except Exception as e:
            self.logger.error(f"❌ Error during cleanup: {e}")

def main():
    """Función principal - Botón de encendido"""
    print("🔌 Starting WoldVirtual Crypto 3D - Power Button...")
    
    # Crear y ejecutar aplicación
    app = WoldVirtualCrypto3D()
    app.start()

if __name__ == "__main__":
    main()