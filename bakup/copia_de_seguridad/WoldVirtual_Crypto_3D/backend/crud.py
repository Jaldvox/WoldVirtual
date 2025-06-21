"""Operaciones CRUD para la base de datos."""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import hashlib

from . import models, schemas

# Operaciones de Usuario
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Obtener un usuario por ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Obtener un usuario por email."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.User]:
    """Obtener lista de usuarios."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Crear un nuevo usuario."""
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = models.User(
        email=user.email,
        username=user.username,
        wallet_address=user.wallet_address,
        hashed_password=hashed_password,
        created_at=datetime.now(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Operaciones de Activo
def get_asset(db: Session, asset_id: int) -> Optional[models.Asset]:
    """Obtener un activo por ID."""
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

def get_assets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    asset_type: Optional[str] = None
) -> List[models.Asset]:
    """Obtener lista de activos."""
    query = db.query(models.Asset)
    if asset_type:
        query = query.filter(models.Asset.asset_type == asset_type)
    return query.offset(skip).limit(limit).all()

def create_asset(db: Session, asset: schemas.AssetCreate) -> models.Asset:
    """Crear un nuevo activo."""
    db_asset = models.Asset(
        **asset.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# Operaciones de Escena
def get_scene(db: Session, scene_id: int) -> Optional[models.Scene]:
    """Obtener una escena por ID."""
    return db.query(models.Scene).filter(models.Scene.id == scene_id).first()

def get_scenes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    creator_id: Optional[int] = None
) -> List[models.Scene]:
    """Obtener lista de escenas."""
    query = db.query(models.Scene)
    if creator_id:
        query = query.filter(models.Scene.creator_id == creator_id)
    return query.offset(skip).limit(limit).all()

def create_scene(db: Session, scene: schemas.SceneCreate) -> models.Scene:
    """Crear una nueva escena."""
    db_scene = models.Scene(
        **scene.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_scene)
    db.commit()
    db.refresh(db_scene)
    return db_scene

# Operaciones de Transacción
def get_transaction(
    db: Session, transaction_id: int
) -> Optional[models.Transaction]:
    """Obtener una transacción por ID."""
    return db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()

def get_transactions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None
) -> List[models.Transaction]:
    """Obtener lista de transacciones."""
    query = db.query(models.Transaction)
    if user_id:
        query = query.filter(
            (models.Transaction.sender_id == user_id) |
            (models.Transaction.receiver_id == user_id)
        )
    return query.offset(skip).limit(limit).all()

def create_transaction(
    db: Session, transaction: schemas.TransactionCreate
) -> models.Transaction:
    """Crear una nueva transacción."""
    db_transaction = models.Transaction(
        **transaction.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction 