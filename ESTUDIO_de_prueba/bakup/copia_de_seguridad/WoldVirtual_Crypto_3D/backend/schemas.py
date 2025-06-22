"""Esquemas Pydantic para la validación de datos."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

# Esquemas de Usuario
class UserBase(BaseModel):
    """Esquema base de usuario."""
    email: EmailStr
    username: str
    wallet_address: str

class UserCreate(UserBase):
    """Esquema para crear usuario."""
    password: str

class User(UserBase):
    """Esquema de usuario."""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    avatar_url: Optional[str] = None
    theme: str = "light"
    language: str = "es"
    total_transactions: int = 0
    reputation_score: float = 0.0

    class Config:
        """Configuración del modelo."""
        orm_mode = True

# Esquemas de Activo
class AssetBase(BaseModel):
    """Esquema base de activo."""
    name: str
    description: str
    asset_type: str
    creator_id: int
    file_url: str

class AssetCreate(AssetBase):
    """Esquema para crear activo."""
    pass

class Asset(AssetBase):
    """Esquema de activo."""
    id: int
    metadata: Dict = {}
    tags: List[str] = []
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    blockchain: str = "ethereum"
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    views: int = 0
    downloads: int = 0
    price: float = 0.0
    currency: str = "ETH"
    is_for_sale: bool = False

    class Config:
        """Configuración del modelo."""
        orm_mode = True

# Esquemas de Escena
class SceneBase(BaseModel):
    """Esquema base de escena."""
    name: str
    description: str
    creator_id: int
    scene_file_url: str

class SceneCreate(SceneBase):
    """Esquema para crear escena."""
    pass

class Scene(SceneBase):
    """Esquema de escena."""
    id: int
    width: int = 1000
    height: int = 1000
    depth: int = 1000
    assets: List[str] = []
    objects: List[Dict] = []
    environment: Dict = {}
    metadata: Dict = {}
    tags: List[str] = []
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    blockchain: str = "ethereum"
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    views: int = 0
    visits: int = 0
    price: float = 0.0
    currency: str = "ETH"
    is_for_sale: bool = False

    class Config:
        """Configuración del modelo."""
        orm_mode = True

# Esquemas de Transacción
class TransactionBase(BaseModel):
    """Esquema base de transacción."""
    transaction_type: str
    sender_id: int
    receiver_id: int
    transaction_hash: str

class TransactionCreate(TransactionBase):
    """Esquema para crear transacción."""
    asset_id: Optional[int] = None
    scene_id: Optional[int] = None
    amount: float = 0.0
    currency: str = "ETH"

class Transaction(TransactionBase):
    """Esquema de transacción."""
    id: int
    asset_id: Optional[int] = None
    scene_id: Optional[int] = None
    amount: float = 0.0
    currency: str = "ETH"
    block_number: Optional[int] = None
    block_timestamp: Optional[datetime] = None
    status: str = "pending"
    created_at: datetime
    updated_at: datetime
    metadata: Dict = {}

    class Config:
        """Configuración del modelo."""
        orm_mode = True 