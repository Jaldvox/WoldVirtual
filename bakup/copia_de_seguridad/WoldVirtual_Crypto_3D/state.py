"""
Estado global de la aplicación WoldVirtual Crypto 3D.
Maneja el estado de la aplicación, usuarios, escenas 3D y blockchain.
"""

import reflex as rx
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import json
import logging

logger = logging.getLogger(__name__)

class WoldVirtualState(rx.State):
    """Estado principal de la aplicación WoldVirtual Crypto 3D."""
    
    # =============================================================================
    # ESTADO DE LA APLICACIÓN
    # =============================================================================
    
    # Estado general
    app_loaded: bool = False
    current_page: str = "home"
    loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Estado de la interfaz
    sidebar_open: bool = False
    theme: str = "dark"  # "dark" o "light"
    language: str = "es"
    notifications_enabled: bool = True
    
    # =============================================================================
    # ESTADO DEL USUARIO
    # =============================================================================
    
    # Autenticación
    is_authenticated: bool = False
    user_id: Optional[str] = None
    username: str = ""
    email: str = ""
    wallet_address: str = ""
    wallet_connected: bool = False
    
    # Perfil del usuario
    user_avatar: str = ""
    user_reputation: int = 0
    user_level: int = 1
    user_experience: int = 0
    user_balance: Dict[str, float] = {}
    user_assets: List[str] = []
    user_scenes: List[str] = []
    
    # Configuración del usuario
    user_settings: Dict[str, Any] = {
        "theme": "dark",
        "language": "es",
        "notifications": {
            "email": True,
            "push": True,
            "in_app": True
        },
        "privacy": {
            "profile_public": True,
            "show_earnings": False,
            "allow_messages": True
        },
        "performance": {
            "graphics_quality": "high",
            "physics_enabled": True,
            "shadows_enabled": True,
            "particle_effects": True
        }
    }
    
    # =============================================================================
    # ESTADO DE BLOCKCHAIN
    # =============================================================================
    
    # Conexión Web3
    web3_connected: bool = False
    network_id: int = 1
    network_name: str = "Ethereum Mainnet"
    gas_price: int = 20000000000  # 20 Gwei
    gas_limit: int = 300000
    
    # Wallet
    wallet_balance: float = 0.0
    wallet_nonce: int = 0
    pending_transactions: List[Dict[str, Any]] = []
    
    # Contratos
    contracts_loaded: bool = False
    nft_contract_address: str = ""
    marketplace_contract_address: str = ""
    governance_contract_address: str = ""
    staking_contract_address: str = ""
    
    # =============================================================================
    # ESTADO DE ESCENAS 3D
    # =============================================================================
    
    # Escena actual
    current_scene_id: Optional[str] = None
    current_scene_name: str = ""
    current_scene_type: str = "world"
    scene_loaded: bool = False
    scene_loading_progress: float = 0.0
    
    # Configuración de escena
    scene_settings: Dict[str, Any] = {
        "physics_enabled": True,
        "collision_detection": True,
        "shadows_enabled": True,
        "fog_enabled": False,
        "skybox_enabled": True,
        "post_processing": True,
        "max_players": 50,
        "is_public": False
    }
    
    # Cámara
    camera_position: List[float] = [0, 5, 10]
    camera_target: List[float] = [0, 0, 0]
    camera_fov: float = 75.0
    camera_near: float = 0.1
    camera_far: float = 1000.0
    
    # Iluminación
    lighting_settings: Dict[str, Any] = {
        "ambient": {
            "color": "#ffffff",
            "intensity": 0.5
        },
        "directional": {
            "color": "#ffffff",
            "intensity": 0.8,
            "position": [0, 10, 0],
            "cast_shadow": True
        },
        "hemisphere": {
            "sky_color": "#87ceeb",
            "ground_color": "#8b4513",
            "intensity": 0.3
        }
    }
    
    # =============================================================================
    # ESTADO DE ASSETS
    # =============================================================================
    
    # Assets cargados
    loaded_assets: Dict[str, Dict[str, Any]] = {}
    asset_loading_queue: List[str] = []
    asset_loading_progress: Dict[str, float] = {}
    
    # Assets del usuario
    user_owned_assets: List[Dict[str, Any]] = []
    user_created_assets: List[Dict[str, Any]] = []
    user_favorite_assets: List[str] = []
    
    # Marketplace
    marketplace_assets: List[Dict[str, Any]] = []
    marketplace_filters: Dict[str, Any] = {
        "category": "all",
        "price_min": 0,
        "price_max": 1000,
        "sort_by": "newest",
        "search_query": ""
    }
    
    # =============================================================================
    # ESTADO DE INTERACCIÓN
    # =============================================================================
    
    # Chat y comunicación
    chat_messages: List[Dict[str, Any]] = []
    chat_room: Optional[str] = None
    voice_enabled: bool = False
    voice_connected: bool = False
    
    # Interacciones
    selected_object: Optional[str] = None
    hovered_object: Optional[str] = None
    interaction_mode: str = "view"  # "view", "edit", "build"
    
    # =============================================================================
    # ESTADO DE RED
    # =============================================================================
    
    # Conexión de red
    network_connected: bool = False
    network_latency: int = 0
    network_quality: str = "good"  # "poor", "fair", "good", "excellent"
    
    # Jugadores en línea
    online_players: List[Dict[str, Any]] = []
    nearby_players: List[Dict[str, Any]] = []
    
    # =============================================================================
    # MÉTODOS DE INICIALIZACIÓN
    # =============================================================================
    
    def initialize_app(self):
        """Inicializa la aplicación."""
        try:
            self.loading = True
            self.app_loaded = True
            self.load_user_settings()
            self.load_scene_settings()
            self.loading = False
            logger.info("Aplicación inicializada correctamente")
        except Exception as e:
            self.error_message = f"Error al inicializar la aplicación: {str(e)}"
            self.loading = False
            logger.error(f"Error al inicializar la aplicación: {e}")
    
    def load_user_settings(self):
        """Carga la configuración del usuario desde localStorage."""
        try:
            # En una implementación real, esto vendría de la base de datos
            # Por ahora usamos valores por defecto
            pass
        except Exception as e:
            logger.error(f"Error al cargar configuración del usuario: {e}")
    
    def load_scene_settings(self):
        """Carga la configuración de la escena."""
        try:
            # Configuración por defecto de la escena
            pass
        except Exception as e:
            logger.error(f"Error al cargar configuración de escena: {e}")
    
    # =============================================================================
    # MÉTODOS DE AUTENTICACIÓN
    # =============================================================================
    
    def connect_wallet(self):
        """Conecta la wallet del usuario."""
        try:
            self.loading = True
            # Aquí implementaremos la conexión real con Web3
            self.wallet_connected = True
            self.wallet_address = "0x1234567890abcdef1234567890abcdef12345678"  # Placeholder
            self.username = f"Usuario_{self.wallet_address[:6]}"
            self.is_authenticated = True
            self.loading = False
            self.success_message = "Wallet conectada correctamente"
            logger.info(f"Wallet conectada: {self.wallet_address}")
        except Exception as e:
            self.error_message = f"Error al conectar wallet: {str(e)}"
            self.loading = False
            logger.error(f"Error al conectar wallet: {e}")
    
    def disconnect_wallet(self):
        """Desconecta la wallet del usuario."""
        try:
            self.wallet_connected = False
            self.wallet_address = ""
            self.is_authenticated = False
            self.success_message = "Wallet desconectada"
            logger.info("Wallet desconectada")
        except Exception as e:
            self.error_message = f"Error al desconectar wallet: {str(e)}"
            logger.error(f"Error al desconectar wallet: {e}")
    
    def update_user_profile(self, profile_data: Dict[str, Any]):
        """Actualiza el perfil del usuario."""
        try:
            for key, value in profile_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.success_message = "Perfil actualizado correctamente"
            logger.info("Perfil de usuario actualizado")
        except Exception as e:
            self.error_message = f"Error al actualizar perfil: {str(e)}"
            logger.error(f"Error al actualizar perfil: {e}")
    
    # =============================================================================
    # MÉTODOS DE ESCENAS 3D
    # =============================================================================
    
    def load_scene(self, scene_id: str, scene_name: str = ""):
        """Carga una escena 3D."""
        try:
            self.loading = True
            self.current_scene_id = scene_id
            self.current_scene_name = scene_name or f"Escena {scene_id}"
            self.scene_loaded = False
            self.scene_loading_progress = 0.0
            
            # Simular carga progresiva
            self.scene_loading_progress = 25.0
            self.scene_loading_progress = 50.0
            self.scene_loading_progress = 75.0
            self.scene_loading_progress = 100.0
            
        self.scene_loaded = True
            self.loading = False
            self.success_message = f"Escena '{self.current_scene_name}' cargada"
            logger.info(f"Escena cargada: {scene_id}")
        except Exception as e:
            self.error_message = f"Error al cargar escena: {str(e)}"
            self.loading = False
            logger.error(f"Error al cargar escena: {e}")
    
    def update_camera(self, position: List[float], target: List[float]):
        """Actualiza la posición y objetivo de la cámara."""
        try:
        self.camera_position = position
        self.camera_target = target
            logger.debug(f"Cámara actualizada: pos={position}, target={target}")
        except Exception as e:
            logger.error(f"Error al actualizar cámara: {e}")
    
    def update_scene_settings(self, settings: Dict[str, Any]):
        """Actualiza la configuración de la escena."""
        try:
            self.scene_settings.update(settings)
            self.success_message = "Configuración de escena actualizada"
            logger.info("Configuración de escena actualizada")
        except Exception as e:
            self.error_message = f"Error al actualizar configuración: {str(e)}"
            logger.error(f"Error al actualizar configuración de escena: {e}")
    
    # =============================================================================
    # MÉTODOS DE ASSETS
    # =============================================================================
    
    def load_asset(self, asset_id: str, asset_type: str = "model"):
        """Carga un asset en la escena."""
        try:
            self.asset_loading_queue.append(asset_id)
            self.asset_loading_progress[asset_id] = 0.0
            
            # Simular carga progresiva
            self.asset_loading_progress[asset_id] = 50.0
            self.asset_loading_progress[asset_id] = 100.0
            
            self.loaded_assets[asset_id] = {
                "id": asset_id,
                "type": asset_type,
                "loaded": True,
                "position": [0, 0, 0],
                "rotation": [0, 0, 0],
                "scale": [1, 1, 1]
            }
            
            self.asset_loading_queue.remove(asset_id)
            del self.asset_loading_progress[asset_id]
            
            self.success_message = f"Asset '{asset_id}' cargado"
            logger.info(f"Asset cargado: {asset_id}")
        except Exception as e:
            self.error_message = f"Error al cargar asset: {str(e)}"
            logger.error(f"Error al cargar asset: {e}")
    
    def update_asset_position(self, asset_id: str, position: List[float]):
        """Actualiza la posición de un asset."""
        try:
            if asset_id in self.loaded_assets:
                self.loaded_assets[asset_id]["position"] = position
                logger.debug(f"Posición de asset actualizada: {asset_id} -> {position}")
        except Exception as e:
            logger.error(f"Error al actualizar posición de asset: {e}")
    
    def remove_asset(self, asset_id: str):
        """Remueve un asset de la escena."""
        try:
            if asset_id in self.loaded_assets:
                del self.loaded_assets[asset_id]
                self.success_message = f"Asset '{asset_id}' removido"
                logger.info(f"Asset removido: {asset_id}")
        except Exception as e:
            self.error_message = f"Error al remover asset: {str(e)}"
            logger.error(f"Error al remover asset: {e}")
    
    # =============================================================================
    # MÉTODOS DE MARKETPLACE
    # =============================================================================
    
    def load_marketplace_assets(self, filters: Optional[Dict[str, Any]] = None):
        """Carga assets del marketplace."""
        try:
            self.loading = True
            if filters:
                self.marketplace_filters.update(filters)
            
            # Aquí se cargarían los assets desde la API
            self.marketplace_assets = [
                {
                    "id": "asset_1",
                    "name": "Modelo 3D Premium",
                    "type": "model",
                    "price": 0.1,
                    "currency": "ETH",
                    "creator": "0x123...",
                    "thumbnail": "https://example.com/thumb1.jpg",
                    "rating": 4.5,
                    "downloads": 150
                },
                {
                    "id": "asset_2",
                    "name": "Textura HD",
                    "type": "texture",
                    "price": 0.05,
                    "currency": "ETH",
                    "creator": "0x456...",
                    "thumbnail": "https://example.com/thumb2.jpg",
                    "rating": 4.2,
                    "downloads": 89
                }
            ]
            
            self.loading = False
            self.success_message = f"{len(self.marketplace_assets)} assets cargados"
            logger.info(f"Marketplace assets cargados: {len(self.marketplace_assets)}")
        except Exception as e:
            self.error_message = f"Error al cargar marketplace: {str(e)}"
            self.loading = False
            logger.error(f"Error al cargar marketplace: {e}")
    
    def purchase_asset(self, asset_id: str, price: float):
        """Compra un asset del marketplace."""
        try:
            self.loading = True
            # Aquí se implementaría la transacción blockchain
            
            # Simular transacción exitosa
            self.user_owned_assets.append({
                "id": asset_id,
                "purchase_date": datetime.now(timezone.utc).isoformat(),
                "price": price
            })
            
            self.loading = False
            self.success_message = f"Asset '{asset_id}' comprado exitosamente"
            logger.info(f"Asset comprado: {asset_id} por {price} ETH")
        except Exception as e:
            self.error_message = f"Error al comprar asset: {str(e)}"
            self.loading = False
            logger.error(f"Error al comprar asset: {e}")
    
    # =============================================================================
    # MÉTODOS DE INTERFAZ
    # =============================================================================
    
    def toggle_sidebar(self):
        """Alterna la visibilidad de la barra lateral."""
        self.sidebar_open = not self.sidebar_open
    
    def change_theme(self, theme: str):
        """Cambia el tema de la aplicación."""
        try:
            self.theme = theme
            self.user_settings["theme"] = theme
            self.success_message = f"Tema cambiado a {theme}"
            logger.info(f"Tema cambiado: {theme}")
        except Exception as e:
            self.error_message = f"Error al cambiar tema: {str(e)}"
            logger.error(f"Error al cambiar tema: {e}")
    
    def change_language(self, language: str):
        """Cambia el idioma de la aplicación."""
        try:
            self.language = language
            self.user_settings["language"] = language
            self.success_message = f"Idioma cambiado a {language}"
            logger.info(f"Idioma cambiado: {language}")
        except Exception as e:
            self.error_message = f"Error al cambiar idioma: {str(e)}"
            logger.error(f"Error al cambiar idioma: {e}")
    
    def navigate_to(self, page: str):
        """Navega a una página específica."""
        try:
            self.current_page = page
            logger.info(f"Navegación a: {page}")
        except Exception as e:
            logger.error(f"Error en navegación: {e}")
    
    def clear_messages(self):
        """Limpia los mensajes de error y éxito."""
        self.error_message = ""
        self.success_message = ""
    
    # =============================================================================
    # MÉTODOS DE RED
    # =============================================================================
    
    def update_network_status(self, connected: bool, latency: int = 0):
        """Actualiza el estado de la conexión de red."""
        try:
            self.network_connected = connected
            self.network_latency = latency
            
            if latency < 50:
                self.network_quality = "excellent"
            elif latency < 100:
                self.network_quality = "good"
            elif latency < 200:
                self.network_quality = "fair"
            else:
                self.network_quality = "poor"
                
            logger.debug(f"Estado de red actualizado: connected={connected}, latency={latency}ms")
        except Exception as e:
            logger.error(f"Error al actualizar estado de red: {e}")
    
    def update_online_players(self, players: List[Dict[str, Any]]):
        """Actualiza la lista de jugadores en línea."""
        try:
            self.online_players = players
            logger.debug(f"Jugadores en línea actualizados: {len(players)}")
        except Exception as e:
            logger.error(f"Error al actualizar jugadores en línea: {e}")
    
    # =============================================================================
    # MÉTODOS DE UTILIDAD
    # =============================================================================
    
    def get_asset_by_id(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un asset por su ID."""
        return self.loaded_assets.get(asset_id)
    
    def get_user_asset_count(self) -> int:
        """Obtiene el número de assets del usuario."""
        return len(self.user_owned_assets)
    
    def get_scene_asset_count(self) -> int:
        """Obtiene el número de assets en la escena actual."""
        return len(self.loaded_assets)
    
    def is_asset_owned(self, asset_id: str) -> bool:
        """Verifica si el usuario posee un asset."""
        return any(asset["id"] == asset_id for asset in self.user_owned_assets)
    
    def get_wallet_balance_formatted(self) -> str:
        """Obtiene el balance de la wallet formateado."""
        return f"{self.wallet_balance:.4f} ETH"
    
    def get_loading_progress(self) -> float:
        """Obtiene el progreso general de carga."""
        if not self.asset_loading_progress:
            return 100.0
        
        total_progress = sum(self.asset_loading_progress.values())
        return total_progress / len(self.asset_loading_progress)
    
    def export_state(self) -> Dict[str, Any]:
        """Exporta el estado actual para debugging."""
        return {
            "user": {
                "authenticated": self.is_authenticated,
                "username": self.username,
                "wallet_address": self.wallet_address,
                "balance": self.wallet_balance
            },
            "scene": {
                "current": self.current_scene_id,
                "loaded": self.scene_loaded,
                "assets_count": len(self.loaded_assets)
            },
            "network": {
                "connected": self.network_connected,
                "latency": self.network_latency,
                "quality": self.network_quality
            }
        } 