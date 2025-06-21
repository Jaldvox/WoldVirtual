"""Modelo de escenas 3D para el metaverso WoldVirtual Crypto 3D."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import field
from enum import Enum
import reflex as rx
from reflex import Field


class SceneStatus(str, Enum):
    """Estados de la escena."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class SceneType(str, Enum):
    """Tipos de escenas."""
    GAME = "game"
    EXPERIENCE = "experience"
    GALLERY = "gallery"
    MEETING = "meeting"
    EVENT = "event"
    SHOWROOM = "showroom"
    OTHER = "other"


class Scene(rx.Model):
    """Modelo de escena 3D con gestión completa de contenido y interactividad."""
    
    # Información básica
    name: str = Field(..., description="Nombre de la escena")
    description: str = Field(..., description="Descripción detallada de la escena")
    creator_id: str = Field(..., description="ID del usuario creador")
    scene_type: SceneType = Field(default=SceneType.EXPERIENCE, description="Tipo de escena")
    
    # Estado y visibilidad
    status: SceneStatus = SceneStatus.DRAFT
    is_public: bool = False
    is_featured: bool = False
    is_template: bool = False  # Si es una plantilla reutilizable
    
    # Configuración de la escena
    width: int = 1000  # Ancho en unidades del mundo
    height: int = 1000  # Alto en unidades del mundo
    depth: int = 1000  # Profundidad en unidades del mundo
    max_players: int = 50  # Máximo número de jugadores simultáneos
    
    # Contenido y assets
    assets: List[str] = field(default_factory=list)  # IDs de los activos en la escena
    objects: List[Dict[str, Any]] = field(default_factory=list)  # Objetos y sus transformaciones
    environment: Dict[str, Any] = field(default_factory=dict)  # Configuración del entorno
    
    # Metadatos y categorización
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    
    # Blockchain y NFT
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    blockchain: str = "ethereum"
    network: str = "mainnet"
    
    # Archivos y URLs
    scene_file_url: str = Field(..., description="URL al archivo de la escena en IPFS")
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    metadata_url: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    
    # Estadísticas y métricas
    views: int = 0
    visits: int = 0
    likes: int = 0
    shares: int = 0
    total_playtime: int = 0  # Tiempo total de juego en segundos
    
    # Precios y mercado
    price: float = 0.0
    currency: str = "ETH"
    is_for_sale: bool = False
    royalty_percentage: float = 2.5
    
    # Configuración de acceso
    access_type: str = "public"  # public, private, whitelist, token_gated
    whitelist: List[str] = field(default_factory=list)  # Lista de usuarios permitidos
    required_tokens: List[Dict[str, Any]] = field(default_factory=list)  # Tokens requeridos para acceso
    
    # Configuración de rendimiento
    complexity_score: float = 0.0  # Score de complejidad de la escena
    optimization_level: str = "medium"  # low, medium, high
    recommended_specs: Dict[str, Any] = field(default_factory=dict)
    
    class Config:
        """Configuración del modelo."""
        table = "scenes"
        indexes = [
            ("creator_id",),
            ("scene_type",),
            ("status",),
            ("is_public",),
            ("is_for_sale",),
            ("access_type",),
            ("created_at",),
            ("views",),
            ("complexity_score",)
        ]
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_data()
    
    def _validate_data(self):
        """Valida los datos básicos de la escena."""
        if not self.name or len(self.name) < 2:
            raise ValueError("Nombre de la escena debe tener al menos 2 caracteres")
        
        if not self.description or len(self.description) < 10:
            raise ValueError("Descripción debe tener al menos 10 caracteres")
        
        if not self.scene_file_url:
            raise ValueError("URL del archivo de escena es requerida")
        
        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")
        
        if self.max_players < 1:
            raise ValueError("El máximo de jugadores debe ser al menos 1")
    
    def publish(self) -> bool:
        """Publica la escena."""
        if self.status == SceneStatus.DRAFT:
            self.status = SceneStatus.PUBLISHED
            self.is_public = True
            self.published_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def archive(self) -> bool:
        """Archiva la escena."""
        if self.status == SceneStatus.PUBLISHED:
            self.status = SceneStatus.ARCHIVED
            self.is_public = False
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def delete(self) -> bool:
        """Marca la escena como eliminada."""
        self.status = SceneStatus.DELETED
        self.is_public = False
        self.is_for_sale = False
        self.updated_at = datetime.utcnow()
        return True
    
    def add_asset(self, asset_id: str, transform: Dict[str, Any]) -> bool:
        """Añade un activo a la escena."""
        if asset_id and asset_id not in self.assets:
            self.assets.append(asset_id)
            self.objects.append({
                "asset_id": asset_id,
                "transform": transform,
                "added_at": datetime.utcnow().isoformat()
            })
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def remove_asset(self, asset_id: str) -> bool:
        """Elimina un activo de la escena."""
        if asset_id in self.assets:
            self.assets.remove(asset_id)
            self.objects = [obj for obj in self.objects if obj["asset_id"] != asset_id]
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def update_asset_transform(self, asset_id: str, new_transform: Dict[str, Any]) -> bool:
        """Actualiza la transformación de un activo en la escena."""
        for obj in self.objects:
            if obj["asset_id"] == asset_id:
                obj["transform"] = new_transform
                obj["updated_at"] = datetime.utcnow().isoformat()
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def update_environment(self, new_environment: Dict[str, Any]) -> None:
        """Actualiza la configuración del entorno."""
        self.environment.update(new_environment)
        self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> bool:
        """Añade una etiqueta a la escena."""
        if tag and tag not in self.tags:
            self.tags.append(tag.lower())
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def remove_tag(self, tag: str) -> bool:
        """Elimina una etiqueta de la escena."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def add_category(self, category: str) -> bool:
        """Añade una categoría a la escena."""
        if category and category not in self.categories:
            self.categories.append(category)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def set_price(self, price: float, currency: str = "ETH") -> None:
        """Establece el precio de la escena."""
        if price >= 0:
            self.price = price
            self.currency = currency
            self.is_for_sale = price > 0
            self.updated_at = datetime.utcnow()
    
    def remove_from_sale(self) -> None:
        """Retira la escena de la venta."""
        self.is_for_sale = False
        self.price = 0.0
        self.updated_at = datetime.utcnow()
    
    def add_to_whitelist(self, user_id: str) -> bool:
        """Añade un usuario a la whitelist."""
        if user_id and user_id not in self.whitelist:
            self.whitelist.append(user_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def remove_from_whitelist(self, user_id: str) -> bool:
        """Elimina un usuario de la whitelist."""
        if user_id in self.whitelist:
            self.whitelist.remove(user_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def increment_views(self) -> None:
        """Incrementa el contador de vistas."""
        self.views += 1
        self.updated_at = datetime.utcnow()
    
    def increment_visits(self) -> None:
        """Incrementa el contador de visitas."""
        self.visits += 1
        self.last_accessed = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def increment_likes(self) -> None:
        """Incrementa el contador de likes."""
        self.likes += 1
        self.updated_at = datetime.utcnow()
    
    def increment_shares(self) -> None:
        """Incrementa el contador de shares."""
        self.shares += 1
        self.updated_at = datetime.utcnow()
    
    def add_playtime(self, seconds: int) -> None:
        """Añade tiempo de juego a la escena."""
        if seconds > 0:
            self.total_playtime += seconds
            self.updated_at = datetime.utcnow()
    
    def calculate_complexity_score(self) -> float:
        """Calcula el score de complejidad de la escena."""
        base_score = len(self.assets) * 0.1
        object_score = len(self.objects) * 0.05
        size_score = (self.width * self.height * self.depth) / 1000000 * 0.01
        
        self.complexity_score = min(base_score + object_score + size_score, 10.0)
        self.updated_at = datetime.utcnow()
        return self.complexity_score
    
    def check_access_permission(self, user_id: str, user_tokens: List[Dict[str, Any]] = None) -> bool:
        """Verifica si un usuario tiene permiso para acceder a la escena."""
        if self.access_type == "public":
            return True
        
        if self.access_type == "private" and user_id == self.creator_id:
            return True
        
        if self.access_type == "whitelist" and user_id in self.whitelist:
            return True
        
        if self.access_type == "token_gated" and user_tokens:
            # Verificar si el usuario tiene los tokens requeridos
            for required_token in self.required_tokens:
                for user_token in user_tokens:
                    if (user_token.get("contract_address") == required_token.get("contract_address") and
                        user_token.get("token_id") == required_token.get("token_id")):
                        return True
        
        return False
    
    def get_public_info(self) -> Dict[str, Any]:
        """Retorna información pública de la escena."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "scene_type": self.scene_type.value,
            "creator_id": self.creator_id,
            "thumbnail_url": self.thumbnail_url,
            "preview_url": self.preview_url,
            "tags": self.tags,
            "categories": self.categories,
            "price": self.price,
            "currency": self.currency,
            "is_for_sale": self.is_for_sale,
            "views": self.views,
            "visits": self.visits,
            "likes": self.likes,
            "max_players": self.max_players,
            "complexity_score": self.complexity_score,
            "created_at": self.created_at,
            "published_at": self.published_at
        }
    
    def get_scene_data(self) -> Dict[str, Any]:
        """Retorna los datos completos de la escena para el renderizado."""
        return {
            "id": self.id,
            "name": self.name,
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "depth": self.depth
            },
            "environment": self.environment,
            "objects": self.objects,
            "assets": self.assets,
            "settings": {
                "max_players": self.max_players,
                "optimization_level": self.optimization_level,
                "recommended_specs": self.recommended_specs
            }
        }
    
    @property
    def is_published(self) -> bool:
        """Verifica si la escena está publicada."""
        return self.status == SceneStatus.PUBLISHED
    
    @property
    def is_available_for_sale(self) -> bool:
        """Verifica si la escena está disponible para venta."""
        return self.is_published and self.is_for_sale and self.price > 0
    
    @property
    def popularity_score(self) -> float:
        """Calcula un score de popularidad basado en métricas."""
        return (self.views * 0.2) + (self.visits * 0.3) + (self.likes * 0.3) + (self.shares * 0.2)
    
    @property
    def average_playtime(self) -> float:
        """Calcula el tiempo promedio de juego por visita."""
        return self.total_playtime / max(self.visits, 1) 