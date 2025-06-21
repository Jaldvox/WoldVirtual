"""Modelo de activos digitales para el metaverso WoldVirtual Crypto 3D."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import field
from enum import Enum
import reflex as rx
from reflex import Field


class AssetType(str, Enum):
    """Tipos de activos disponibles."""
    MODEL_3D = "3d_model"
    TEXTURE = "texture"
    SOUND = "sound"
    ANIMATION = "animation"
    SCENE = "scene"
    CHARACTER = "character"
    VEHICLE = "vehicle"
    BUILDING = "building"
    NATURE = "nature"
    EFFECT = "effect"
    OTHER = "other"


class AssetStatus(str, Enum):
    """Estados del activo."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Asset(rx.Model):
    """Modelo de activo digital (NFT) con gestión completa de metadatos."""
    
    # Información básica
    name: str = Field(..., description="Nombre del activo")
    description: str = Field(..., description="Descripción detallada del activo")
    asset_type: AssetType = Field(..., description="Tipo de activo")
    creator_id: str = Field(..., description="ID del usuario creador")
    
    # Estado y visibilidad
    status: AssetStatus = AssetStatus.DRAFT
    is_public: bool = False
    is_featured: bool = False
    
    # Metadatos y categorización
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    
    # Información técnica
    file_size: Optional[int] = None  # Tamaño en bytes
    file_format: Optional[str] = None  # Formato del archivo
    dimensions: Optional[Dict[str, float]] = None  # Dimensiones 3D
    polygon_count: Optional[int] = None  # Número de polígonos
    texture_resolution: Optional[str] = None  # Resolución de texturas
    
    # Blockchain y NFT
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    blockchain: str = "ethereum"
    network: str = "mainnet"  # mainnet, testnet, polygon, etc.
    
    # Archivos y URLs
    file_url: str = Field(..., description="URL al archivo en IPFS")
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    metadata_url: Optional[str] = None  # URL a metadatos JSON
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    # Estadísticas y métricas
    views: int = 0
    downloads: int = 0
    likes: int = 0
    shares: int = 0
    
    # Precios y mercado
    price: float = 0.0
    currency: str = "ETH"
    is_for_sale: bool = False
    royalty_percentage: float = 2.5  # Porcentaje de regalías
    
    # Propiedad y licencias
    owner_id: Optional[str] = None
    license_type: str = "commercial"  # commercial, personal, creative_commons
    license_url: Optional[str] = None
    
    class Config:
        """Configuración del modelo."""
        table = "assets"
        indexes = [
            ("creator_id",),
            ("asset_type",),
            ("status",),
            ("is_public",),
            ("is_for_sale",),
            ("price",),
            ("created_at",),
            ("views",)
        ]
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_data()
    
    def _validate_data(self):
        """Valida los datos básicos del activo."""
        if not self.name or len(self.name) < 2:
            raise ValueError("Nombre del activo debe tener al menos 2 caracteres")
        
        if not self.description or len(self.description) < 10:
            raise ValueError("Descripción debe tener al menos 10 caracteres")
        
        if not self.file_url:
            raise ValueError("URL del archivo es requerida")
        
        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")
    
    def publish(self) -> bool:
        """Publica el activo."""
        if self.status == AssetStatus.DRAFT:
            self.status = AssetStatus.PUBLISHED
            self.is_public = True
            self.published_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def archive(self) -> bool:
        """Archiva el activo."""
        if self.status == AssetStatus.PUBLISHED:
            self.status = AssetStatus.ARCHIVED
            self.is_public = False
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def delete(self) -> bool:
        """Marca el activo como eliminado."""
        self.status = AssetStatus.DELETED
        self.is_public = False
        self.is_for_sale = False
        self.updated_at = datetime.utcnow()
        return True
    
    def update_metadata(self, new_metadata: Dict[str, Any]) -> None:
        """Actualiza los metadatos del activo."""
        self.metadata.update(new_metadata)
        self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> bool:
        """Añade una etiqueta al activo."""
        if tag and tag not in self.tags:
            self.tags.append(tag.lower())
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def remove_tag(self, tag: str) -> bool:
        """Elimina una etiqueta del activo."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def add_category(self, category: str) -> bool:
        """Añade una categoría al activo."""
        if category and category not in self.categories:
            self.categories.append(category)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def set_price(self, price: float, currency: str = "ETH") -> None:
        """Establece el precio del activo."""
        if price >= 0:
            self.price = price
            self.currency = currency
            self.is_for_sale = price > 0
            self.updated_at = datetime.utcnow()
    
    def remove_from_sale(self) -> None:
        """Retira el activo de la venta."""
        self.is_for_sale = False
        self.price = 0.0
        self.updated_at = datetime.utcnow()
    
    def transfer_ownership(self, new_owner_id: str) -> bool:
        """Transfiere la propiedad del activo."""
        if new_owner_id and new_owner_id != self.owner_id:
            self.owner_id = new_owner_id
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def increment_views(self) -> None:
        """Incrementa el contador de vistas."""
        self.views += 1
        self.updated_at = datetime.utcnow()
    
    def increment_downloads(self) -> None:
        """Incrementa el contador de descargas."""
        self.downloads += 1
        self.updated_at = datetime.utcnow()
    
    def increment_likes(self) -> None:
        """Incrementa el contador de likes."""
        self.likes += 1
        self.updated_at = datetime.utcnow()
    
    def increment_shares(self) -> None:
        """Incrementa el contador de shares."""
        self.shares += 1
        self.updated_at = datetime.utcnow()
    
    def set_technical_info(self, **kwargs) -> None:
        """Establece información técnica del activo."""
        allowed_fields = ['file_size', 'file_format', 'dimensions', 
                         'polygon_count', 'texture_resolution']
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)
        
        self.updated_at = datetime.utcnow()
    
    def get_public_info(self) -> Dict[str, Any]:
        """Retorna información pública del activo."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "asset_type": self.asset_type.value,
            "creator_id": self.creator_id,
            "thumbnail_url": self.thumbnail_url,
            "preview_url": self.preview_url,
            "tags": self.tags,
            "categories": self.categories,
            "price": self.price,
            "currency": self.currency,
            "is_for_sale": self.is_for_sale,
            "views": self.views,
            "likes": self.likes,
            "created_at": self.created_at,
            "published_at": self.published_at
        }
    
    def get_nft_metadata(self) -> Dict[str, Any]:
        """Retorna metadatos para NFT."""
        return {
            "name": self.name,
            "description": self.description,
            "image": self.thumbnail_url or self.preview_url,
            "external_url": f"https://woldvirtual.com/asset/{self.id}",
            "attributes": [
                {"trait_type": "Type", "value": self.asset_type.value},
                {"trait_type": "Creator", "value": self.creator_id},
                {"trait_type": "Views", "value": self.views},
                {"trait_type": "Likes", "value": self.likes},
                {"trait_type": "Downloads", "value": self.downloads}
            ] + [
                {"trait_type": tag.title(), "value": "Yes"} 
                for tag in self.tags[:5]  # Máximo 5 tags como atributos
            ]
        }
    
    @property
    def is_published(self) -> bool:
        """Verifica si el activo está publicado."""
        return self.status == AssetStatus.PUBLISHED
    
    @property
    def is_available_for_sale(self) -> bool:
        """Verifica si el activo está disponible para venta."""
        return self.is_published and self.is_for_sale and self.price > 0
    
    @property
    def popularity_score(self) -> float:
        """Calcula un score de popularidad basado en métricas."""
        return (self.views * 0.3) + (self.likes * 0.4) + (self.downloads * 0.3) 