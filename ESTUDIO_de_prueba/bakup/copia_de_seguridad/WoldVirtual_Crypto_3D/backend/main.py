"""Backend principal de WoldVirtual."""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import asyncio

from .database import get_db
from . import models, schemas, crud
from .communication import communication_manager
from .connections import connection_manager
from .events import event_manager, register_system_events

app = FastAPI(title="WoldVirtual API")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicio
@app.on_event("startup")
async def startup_event():
    """Eventos de inicio de la aplicación."""
    # Registrar eventos del sistema
    await register_system_events()
    
    # Iniciar procesador de mensajes
    asyncio.create_task(communication_manager.process_messages())
    
    # Notificar inicio
    await event_manager.trigger_event(
        'system_startup',
        {'status': 'initialized'}
    )

# Eventos de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """Eventos de cierre de la aplicación."""
    # Notificar cierre
    await event_manager.trigger_event(
        'system_shutdown',
        {'status': 'shutting_down'}
    )
    
    # Cerrar conexiones activas
    active_connections = connection_manager.get_active_connections()
    for conn_id in active_connections:
        await connection_manager.close_connection(conn_id)

# Rutas de usuarios
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
        
    new_user = crud.create_user(db=db, user=user)
    
    # Notificar creación de usuario
    await event_manager.trigger_event(
        'user_created',
        {'user_id': new_user.id, 'email': new_user.email}
    )
    
    return new_user

@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de usuarios."""
    users = crud.get_users(db, skip=skip, limit=limit)
    
    # Notificar consulta de usuarios
    await event_manager.trigger_event(
        'users_queried',
        {'count': len(users)}
    )
    
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario específico."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    # Notificar consulta de usuario
    await event_manager.trigger_event(
        'user_queried',
        {'user_id': user_id}
    )
    
    return db_user

# Rutas de activos
@app.post("/assets/", response_model=schemas.Asset)
async def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    """Crear un nuevo activo."""
    new_asset = crud.create_asset(db=db, asset=asset)
    
    # Notificar creación de activo
    await event_manager.trigger_event(
        'asset_created',
        {'asset_id': new_asset.id, 'type': new_asset.asset_type}
    )
    
    return new_asset

@app.get("/assets/", response_model=List[schemas.Asset])
async def read_assets(
    skip: int = 0,
    limit: int = 100,
    asset_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de activos."""
    assets = crud.get_assets(db, skip=skip, limit=limit, asset_type=asset_type)
    
    # Notificar consulta de activos
    await event_manager.trigger_event(
        'assets_queried',
        {'count': len(assets), 'type': asset_type}
    )
    
    return assets

@app.get("/assets/{asset_id}", response_model=schemas.Asset)
async def read_asset(asset_id: int, db: Session = Depends(get_db)):
    """Obtener un activo específico."""
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Activo no encontrado")
        
    # Notificar consulta de activo
    await event_manager.trigger_event(
        'asset_queried',
        {'asset_id': asset_id}
    )
    
    return db_asset

# Rutas de escenas
@app.post("/scenes/", response_model=schemas.Scene)
async def create_scene(scene: schemas.SceneCreate, db: Session = Depends(get_db)):
    """Crear una nueva escena."""
    new_scene = crud.create_scene(db=db, scene=scene)
    
    # Notificar creación de escena
    await event_manager.trigger_event(
        'scene_created',
        {'scene_id': new_scene.id}
    )
    
    return new_scene

@app.get("/scenes/", response_model=List[schemas.Scene])
async def read_scenes(
    skip: int = 0,
    limit: int = 100,
    creator_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de escenas."""
    scenes = crud.get_scenes(db, skip=skip, limit=limit, creator_id=creator_id)
    
    # Notificar consulta de escenas
    await event_manager.trigger_event(
        'scenes_queried',
        {'count': len(scenes), 'creator_id': creator_id}
    )
    
    return scenes

@app.get("/scenes/{scene_id}", response_model=schemas.Scene)
async def read_scene(scene_id: int, db: Session = Depends(get_db)):
    """Obtener una escena específica."""
    db_scene = crud.get_scene(db, scene_id=scene_id)
    if db_scene is None:
        raise HTTPException(status_code=404, detail="Escena no encontrada")
        
    # Notificar consulta de escena
    await event_manager.trigger_event(
        'scene_queried',
        {'scene_id': scene_id}
    )
    
    return db_scene

# Rutas de transacciones
@app.post("/transactions/", response_model=schemas.Transaction)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva transacción."""
    new_transaction = crud.create_transaction(db=db, transaction=transaction)
    
    # Notificar creación de transacción
    await event_manager.trigger_event(
        'transaction_created',
        {
            'transaction_id': new_transaction.id,
            'type': new_transaction.transaction_type
        }
    )
    
    return new_transaction

@app.get("/transactions/", response_model=List[schemas.Transaction])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de transacciones."""
    transactions = crud.get_transactions(
        db, skip=skip, limit=limit, user_id=user_id
    )
    
    # Notificar consulta de transacciones
    await event_manager.trigger_event(
        'transactions_queried',
        {'count': len(transactions), 'user_id': user_id}
    )
    
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
async def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Obtener una transacción específica."""
    db_transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
        
    # Notificar consulta de transacción
    await event_manager.trigger_event(
        'transaction_queried',
        {'transaction_id': transaction_id}
    )
    
    return db_transaction

# Rutas de sistema
@app.get("/system/stats")
async def get_system_stats():
    """Obtener estadísticas del sistema."""
    return {
        'communication': communication_manager.get_topic_stats(),
        'connections': connection_manager.get_connection_stats(),
        'events': event_manager.get_event_stats()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 