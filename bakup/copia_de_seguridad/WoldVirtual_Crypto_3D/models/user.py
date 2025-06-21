"""Modelo de usuario para el metaverso WoldVirtual Crypto 3D."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import field
import reflex as rx
from reflex import Field


class User(rx.Model):
    """Modelo de usuario del metaverso con gestión de wallet y reputación."""
    
    # Información básica
    username: str = Field(..., description="Nombre de usuario único")
    email: str = Field(..., description="Correo electrónico del usuario")
    wallet_address: str = Field(..., description="Dirección de wallet Ethereum")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Estado de la cuenta
    is_active: bool = True
    is_verified: bool = False
    is_premium: bool = False
    
    # Perfil y preferencias
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    theme: str = "dark"
    language: str = "es"
    timezone: str = "UTC"
    
    # Inventario y posesiones
    owned_assets: List[str] = field(default_factory=list)
    created_scenes: List[str] = field(default_factory=list)
    favorite_scenes: List[str] = field(default_factory=list)
    
    # Estadísticas y métricas
    total_transactions: int = 0
    reputation_score: float = 0.0
    total_earnings: float = 0.0
    total_spent: float = 0.0
    
    # Configuración de privacidad
    is_profile_public: bool = True
    show_earnings: bool = False
    allow_messages: bool = True
    
    # Metadatos adicionales
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    class Config:
        """Configuración del modelo."""
        table = "users"
        indexes = [
            ("username",),
            ("email",),
            ("wallet_address",),
            ("is_active",),
            ("reputation_score",)
        ]
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_data()
    
    def _validate_data(self):
        """Valida los datos básicos del usuario."""
        if not self.username or len(self.username) < 3:
            raise ValueError("Username debe tener al menos 3 caracteres")
        
        if not self.email or "@" not in self.email:
            raise ValueError("Email debe ser válido")
        
        if not self.wallet_address or not self.wallet_address.startswith("0x"):
            raise ValueError("Wallet address debe ser una dirección Ethereum válida")
    
    def update_last_login(self):
        """Actualiza el timestamp del último login."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def verify_wallet(self, signature: str, message: str) -> bool:
        """Verifica la firma de la wallet del usuario."""
        # TODO: Implementar verificación criptográfica real
        # Por ahora retorna True para desarrollo
        self.is_verified = True
        self.updated_at = datetime.utcnow()
        return True
    
    def add_asset(self, asset_id: str) -> bool:
        """Añade un activo al inventario del usuario."""
        if asset_id and asset_id not in self.owned_assets:
            self.owned_assets.append(asset_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def remove_asset(self, asset_id: str) -> bool:
        """Elimina un activo del inventario del usuario."""
        if asset_id in self.owned_assets:
            self.owned_assets.remove(asset_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def create_scene(self, scene_id: str) -> bool:
        """Registra una nueva escena creada por el usuario."""
        if scene_id and scene_id not in self.created_scenes:
            self.created_scenes.append(scene_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def add_favorite_scene(self, scene_id: str) -> bool:
        """Añade una escena a favoritos."""
        if scene_id and scene_id not in self.favorite_scenes:
            self.favorite_scenes.append(scene_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def remove_favorite_scene(self, scene_id: str) -> bool:
        """Elimina una escena de favoritos."""
        if scene_id in self.favorite_scenes:
            self.favorite_scenes.remove(scene_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def update_reputation(self, score: float) -> None:
        """Actualiza la puntuación de reputación del usuario."""
        if -1.0 <= score <= 1.0:
            # Promedio ponderado para suavizar cambios
            self.reputation_score = (self.reputation_score * 0.7) + (score * 0.3)
            self.updated_at = datetime.utcnow()
    
    def add_earnings(self, amount: float) -> None:
        """Añade ganancias al usuario."""
        if amount > 0:
            self.total_earnings += amount
            self.updated_at = datetime.utcnow()
    
    def add_expense(self, amount: float) -> None:
        """Añade gastos al usuario."""
        if amount > 0:
            self.total_spent += amount
            self.updated_at = datetime.utcnow()
    
    def increment_transactions(self) -> None:
        """Incrementa el contador de transacciones."""
        self.total_transactions += 1
        self.updated_at = datetime.utcnow()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Actualiza metadatos específicos del usuario."""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def get_public_profile(self) -> Dict[str, Any]:
        """Retorna información pública del perfil."""
        return {
            "username": self.username,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "created_at": self.created_at,
            "reputation_score": self.reputation_score,
            "total_transactions": self.total_transactions,
            "owned_assets_count": len(self.owned_assets),
            "created_scenes_count": len(self.created_scenes),
            "is_verified": self.is_verified,
            "is_premium": self.is_premium
        }
    
    @property
    def is_new_user(self) -> bool:
        """Verifica si el usuario es nuevo (menos de 7 días)."""
        return (datetime.utcnow() - self.created_at).days < 7
    
    @property
    def has_activity(self) -> bool:
        """Verifica si el usuario tiene actividad reciente."""
        return self.total_transactions > 0 or len(self.created_scenes) > 0 