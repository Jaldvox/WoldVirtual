# backend/models.py

"""Modelos de la base de datos."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    """Modelo de usuario."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    avatar_url = Column(String, nullable=True)
    theme = Column(String, default="light")
    language = Column(String, default="es")
    total_transactions = Column(Integer, default=0)
    reputation_score = Column(Float, default=0.0)

    # Relaciones
    assets = relationship("Asset", back_populates="creator")
    scenes = relationship("Scene", back_populates="creator")
    sent_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender"
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_id",
        back_populates="receiver"
    )

class Asset(Base):
    """Modelo de activo."""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    asset_type = Column(String, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    file_url = Column(String)
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
    token_id = Column(String, nullable=True)
    contract_address = Column(String, nullable=True)
    blockchain = Column(String, default="ethereum")
    thumbnail_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    views = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    currency = Column(String, default="ETH")
    is_for_sale = Column(Boolean, default=False)

    # Relaciones
    creator = relationship("User", back_populates="assets")
    transactions = relationship("Transaction", back_populates="asset")

class Scene(Base):
    """Modelo de escena."""
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    scene_file_url = Column(String)
    width = Column(Integer, default=1000)
    height = Column(Integer, default=1000)
    depth = Column(Integer, default=1000)
    assets = Column(JSON, default=[])
    objects = Column(JSON, default=[])
    environment = Column(JSON, default={})
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
    token_id = Column(String, nullable=True)
    contract_address = Column(String, nullable=True)
    blockchain = Column(String, default="ethereum")
    thumbnail_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    views = Column(Integer, default=0)
    visits = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    currency = Column(String, default="ETH")
    is_for_sale = Column(Boolean, default=False)

    # Relaciones
    creator = relationship("User", back_populates="scenes")
    transactions = relationship("Transaction", back_populates="scene")

class Transaction(Base):
    """Modelo de transacción."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"), nullable=True)
    amount = Column(Float, default=0.0)
    currency = Column(String, default="ETH")
    transaction_hash = Column(String, unique=True, index=True)
    block_number = Column(Integer, nullable=True)
    block_timestamp = Column(DateTime, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    metadata = Column(JSON, default={})

    # Relaciones
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")
    asset = relationship("Asset", back_populates="transactions")
    scene = relationship("Scene", back_populates="transactions") 