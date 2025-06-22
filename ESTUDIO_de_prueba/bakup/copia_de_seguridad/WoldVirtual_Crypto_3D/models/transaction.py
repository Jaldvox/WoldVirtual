"""Modelo de transacciones para el metaverso WoldVirtual Crypto 3D."""
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import field
from enum import Enum
import reflex as rx
from reflex import Field


class TransactionType(str, Enum):
    """Tipos de transacciones."""
    PURCHASE = "purchase"
    SALE = "sale"
    TRANSFER = "transfer"
    MINT = "mint"
    BURN = "burn"
    BID = "bid"
    ACCEPT_BID = "accept_bid"
    ROYALTY = "royalty"
    REFUND = "refund"
    OTHER = "other"


class TransactionStatus(str, Enum):
    """Estados de las transacciones."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Transaction(rx.Model):
    """Modelo de transacción blockchain con gestión completa de estados."""
    
    # Información básica
    transaction_type: TransactionType = Field(..., description="Tipo de transacción")
    sender_id: str = Field(..., description="ID del usuario remitente")
    receiver_id: str = Field(..., description="ID del usuario destinatario")
    
    # Detalles de la transacción
    asset_id: Optional[str] = None  # ID del activo involucrado
    scene_id: Optional[str] = None  # ID de la escena involucrada
    amount: float = Field(default=0.0, description="Cantidad de la transacción")
    currency: str = "ETH"
    
    # Información de blockchain
    transaction_hash: str = Field(..., description="Hash de la transacción")
    block_number: Optional[int] = None
    block_timestamp: Optional[datetime] = None
    gas_used: Optional[int] = None
    gas_price: Optional[int] = None
    gas_limit: Optional[int] = None
    
    # Estado y timestamps
    status: TransactionStatus = TransactionStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    
    # Metadatos y contexto
    metadata: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None
    notes: Optional[str] = None
    
    # Información de red
    network: str = "ethereum"
    chain_id: int = 1
    
    # Información de fees y comisiones
    platform_fee: float = 0.0
    creator_royalty: float = 0.0
    gas_fee: float = 0.0
    
    # Información de búsqueda y filtrado
    tags: list = field(default_factory=list)
    
    class Config:
        """Configuración del modelo."""
        table = "transactions"
        indexes = [
            ("transaction_hash",),
            ("sender_id",),
            ("receiver_id",),
            ("transaction_type",),
            ("status",),
            ("created_at",),
            ("asset_id",),
            ("scene_id",),
            ("block_number",)
        ]
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_data()
    
    def _validate_data(self):
        """Valida los datos básicos de la transacción."""
        if not self.transaction_hash:
            raise ValueError("Hash de transacción es requerido")
        
        if not self.sender_id:
            raise ValueError("ID del remitente es requerido")
        
        if not self.receiver_id:
            raise ValueError("ID del destinatario es requerido")
        
        if self.amount < 0:
            raise ValueError("El monto no puede ser negativo")
        
        if self.sender_id == self.receiver_id:
            raise ValueError("El remitente y destinatario no pueden ser el mismo")
    
    def confirm_transaction(self, block_number: int, block_timestamp: datetime, 
                          gas_used: int = None, gas_price: int = None) -> bool:
        """Confirma la transacción con información del bloque."""
        if self.status == TransactionStatus.PENDING:
        self.block_number = block_number
        self.block_timestamp = block_timestamp
            self.gas_used = gas_used
            self.gas_price = gas_price
            self.status = TransactionStatus.CONFIRMED
            self.confirmed_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            
            # Calcular gas fee si se proporciona la información
            if gas_used and gas_price:
                self.gas_fee = (gas_used * gas_price) / 1e18  # Convertir de wei a ETH
            
            return True
        return False
    
    def fail_transaction(self, reason: str = None) -> bool:
        """Marca la transacción como fallida."""
        if self.status == TransactionStatus.PENDING:
            self.status = TransactionStatus.FAILED
            self.failed_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            
            if reason:
                self.notes = f"Failed: {reason}"
            
            return True
        return False
    
    def cancel_transaction(self, reason: str = None) -> bool:
        """Cancela la transacción."""
        if self.status == TransactionStatus.PENDING:
            self.status = TransactionStatus.CANCELLED
            self.updated_at = datetime.utcnow()
            
            if reason:
                self.notes = f"Cancelled: {reason}"
            
            return True
        return False
    
    def expire_transaction(self) -> bool:
        """Marca la transacción como expirada."""
        if self.status == TransactionStatus.PENDING:
            self.status = TransactionStatus.EXPIRED
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def update_status(self, new_status: TransactionStatus, notes: str = None) -> bool:
        """Actualiza el estado de la transacción."""
        if new_status != self.status:
            self.status = new_status
            self.updated_at = datetime.utcnow()
            
            if notes:
                self.notes = notes
            
            # Actualizar timestamps específicos
            if new_status == TransactionStatus.CONFIRMED:
                self.confirmed_at = datetime.utcnow()
            elif new_status == TransactionStatus.FAILED:
                self.failed_at = datetime.utcnow()
            
            return True
        return False
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Añade metadatos específicos a la transacción."""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def update_metadata(self, new_metadata: Dict[str, Any]) -> None:
        """Actualiza los metadatos de la transacción."""
        self.metadata.update(new_metadata)
        self.updated_at = datetime.utcnow()
    
    def add_tag(self, tag: str) -> bool:
        """Añade una etiqueta a la transacción."""
        if tag and tag not in self.tags:
            self.tags.append(tag.lower())
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def set_fees(self, platform_fee: float = 0.0, creator_royalty: float = 0.0) -> None:
        """Establece las comisiones de la transacción."""
        self.platform_fee = max(0.0, platform_fee)
        self.creator_royalty = max(0.0, creator_royalty)
        self.updated_at = datetime.utcnow()
    
    def calculate_total_amount(self) -> float:
        """Calcula el monto total incluyendo fees."""
        return self.amount + self.platform_fee + self.creator_royalty + self.gas_fee
    
    def get_transaction_summary(self) -> Dict[str, Any]:
        """Retorna un resumen de la transacción."""
        return {
            "id": self.id,
            "type": self.transaction_type.value,
            "status": self.status.value,
            "sender": self.sender_id,
            "receiver": self.receiver_id,
            "amount": self.amount,
            "currency": self.currency,
            "total_amount": self.calculate_total_amount(),
            "transaction_hash": self.transaction_hash,
            "block_number": self.block_number,
            "created_at": self.created_at,
            "confirmed_at": self.confirmed_at,
            "asset_id": self.asset_id,
            "scene_id": self.scene_id
        }
    
    def get_blockchain_info(self) -> Dict[str, Any]:
        """Retorna información específica de blockchain."""
        return {
            "transaction_hash": self.transaction_hash,
            "block_number": self.block_number,
            "block_timestamp": self.block_timestamp,
            "gas_used": self.gas_used,
            "gas_price": self.gas_price,
            "gas_limit": self.gas_limit,
            "gas_fee": self.gas_fee,
            "network": self.network,
            "chain_id": self.chain_id
        }
    
    def is_asset_transaction(self) -> bool:
        """Verifica si la transacción involucra un activo."""
        return self.asset_id is not None
    
    def is_scene_transaction(self) -> bool:
        """Verifica si la transacción involucra una escena."""
        return self.scene_id is not None
    
    def is_purchase(self) -> bool:
        """Verifica si es una transacción de compra."""
        return self.transaction_type == TransactionType.PURCHASE
    
    def is_sale(self) -> bool:
        """Verifica si es una transacción de venta."""
        return self.transaction_type == TransactionType.SALE
    
    def is_transfer(self) -> bool:
        """Verifica si es una transacción de transferencia."""
        return self.transaction_type == TransactionType.TRANSFER
    
    @property
    def is_confirmed(self) -> bool:
        """Verifica si la transacción está confirmada."""
        return self.status == TransactionStatus.CONFIRMED
    
    @property
    def is_pending(self) -> bool:
        """Verifica si la transacción está pendiente."""
        return self.status == TransactionStatus.PENDING
    
    @property
    def is_failed(self) -> bool:
        """Verifica si la transacción falló."""
        return self.status == TransactionStatus.FAILED
    
    @property
    def confirmation_time(self) -> Optional[float]:
        """Calcula el tiempo de confirmación en segundos."""
        if self.confirmed_at and self.created_at:
            return (self.confirmed_at - self.created_at).total_seconds()
        return None
    
    @property
    def age_in_seconds(self) -> float:
        """Calcula la edad de la transacción en segundos."""
        return (datetime.utcnow() - self.created_at).total_seconds()
    
    @property
    def age_in_hours(self) -> float:
        """Calcula la edad de la transacción en horas."""
        return self.age_in_seconds / 3600 