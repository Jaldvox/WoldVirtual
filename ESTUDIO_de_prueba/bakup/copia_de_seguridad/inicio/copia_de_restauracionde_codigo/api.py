import reflex as rx
from .state import State

@rx.endpoint()
def get_entidades() -> dict:
    """Devuelve el estado actual de las entidades 3D."""
    return {"entidades": State.entidades}

@rx.endpoint(method="POST")
def evento_cubo_click(id: str):
    """Recibe un evento de clic en un cubo desde el frontend y actualiza el estado."""
    State.on_cubo_click(id)
    return {"ok": True, "nuevo_color": next(e["color"] for e in State.entidades if e["id"] == id)}

# --- ENDPOINTS PREPARADOS PARA BLOCKCHAIN E IPFS ---
# Estos endpoints están preparados pero NO activos. Siguen el patrón de "preparado pero no activo".
# Para activarlos, descomentar el código y asegurar la configuración, dependencias y seguridad.
# Documentación exhaustiva incluida en cada endpoint.

# from .blockchain import BlockchainService
# from .storage import StorageService

# blockchain_service = BlockchainService()
# storage_service = StorageService()

# @rx.endpoint(method="POST")
# def mint_nft(user_address: str, metadata_uri: str, private_key: str) -> dict:
#     """
#     Endpoint para mintear un NFT en la blockchain.
#     Parámetros:
#       - user_address: dirección Ethereum del usuario que recibirá el NFT
#       - metadata_uri: URI de los metadatos (ej. JSON en IPFS)
#       - private_key: clave privada del minteador (NO exponer nunca en frontend)
#     Devuelve:
#       - Hash de la transacción si es exitoso, None si falla.
#     Dependencias internas:
#       - BlockchainService.mint_nft de blockchain.py
#     Advertencias de seguridad:
#       - Este endpoint NO debe exponerse públicamente sin autenticación robusta y validación de entrada.
#       - Nunca exponer claves privadas en frontend o logs.
#     Pasos para activación:
#       1. Instalar web3.py y configurar variables de entorno.
#       2. Descomentar el código y probar en entorno seguro.
#     """
#     # tx_hash = blockchain_service.mint_nft(user_address, metadata_uri, private_key)
#     # return {"tx_hash": tx_hash}
#     return {"tx_hash": None, "msg": "Endpoint preparado, no activo. Ver documentación en el código."}

# @rx.endpoint()
# def get_nft_owner(token_id: int) -> dict:
#     """
#     Consulta el propietario de un NFT.
#     Parámetros:
#       - token_id: ID del token NFT
#     Devuelve:
#       - Dirección Ethereum del propietario, o None si falla.
#     Dependencias internas:
#       - BlockchainService.get_nft_owner de blockchain.py
#     Advertencias de seguridad:
#       - No exponer información sensible sin control de acceso.
#     Pasos para activación:
#       1. Instalar web3.py y configurar variables de entorno.
#       2. Descomentar el código y probar en entorno seguro.
#     """
#     # owner = blockchain_service.get_nft_owner(token_id)
#     # return {"owner": owner}
#     return {"owner": None, "msg": "Endpoint preparado, no activo. Ver documentación en el código."}

# @rx.endpoint(method="POST")
# def upload_to_ipfs(file_path: str) -> dict:
#     """
#     Sube un archivo a IPFS y devuelve el hash CID.
#     Parámetros:
#       - file_path: ruta local al archivo a subir
#     Devuelve:
#       - Hash CID del archivo en IPFS
#     Dependencias internas:
#       - StorageService.upload_to_ipfs de storage.py
#     Advertencias de seguridad:
#       - Validar y sanitizar rutas de archivo.
#       - No exponer este endpoint sin autenticación.
#     Pasos para activación:
#       1. Instalar ipfshttpclient y configurar variables de entorno.
#       2. Descomentar el código y probar en entorno seguro.
#     """
#     # cid = storage_service.upload_to_ipfs(file_path)
#     # return {"cid": cid}
#     return {"cid": "QmFakeHash1234567890", "msg": "Endpoint preparado, no activo. Ver documentación en el código."}

# @rx.endpoint()
# def get_ipfs_url(cid: str) -> dict:
#     """
#     Devuelve la URL pública de un archivo en IPFS.
#     Parámetros:
#       - cid: hash CID del archivo
#     Devuelve:
#       - URL pública accesible vía gateway
#     Dependencias internas:
#       - StorageService.get_ipfs_url de storage.py
#     Advertencias de seguridad:
#       - Validar el formato del CID recibido.
#     Pasos para activación:
#       1. Instalar ipfshttpclient y configurar variables de entorno.
#       2. Descomentar el código y probar en entorno seguro.
#     """
#     # url = storage_service.get_ipfs_url(cid)
#     # return {"url": url}
#     return {"url": f"https://ipfs.io/ipfs/{cid}", "msg": "Endpoint preparado, no activo. Ver documentación en el código."}

# --- FIN ENDPOINTS PREPARADOS ---

# --- ENDPOINTS DE USUARIO ---
@rx.endpoint()
def get_user_public_profile() -> dict:
    """
    Devuelve el perfil público del usuario actual.
    Salida:
      - id, username, avatar_url, reputation_score, is_verified, estado, owned_assets_count, created_at
    """
    return State.obtener_perfil_publico()

@rx.endpoint()
def get_user_private_profile() -> dict:
    """
    Devuelve el perfil privado/completo del usuario actual.
    Salida:
      - todos los campos públicos + email, wallet_address, owned_assets, created_scenes, updated_at
    """
    return State.obtener_perfil_privado()

@rx.endpoint(method="POST")
def update_user_avatar(avatar_url: str) -> dict:
    """
    Actualiza el avatar del usuario actual.
    Entrada:
      - avatar_url: URL del nuevo avatar
    Salida:
      - ok: True si se actualizó
    """
    State.actualizar_avatar(avatar_url)
    return {"ok": True, "avatar_url": avatar_url}

@rx.endpoint(method="POST")
def add_asset_to_user(asset_id: str) -> dict:
    """
    Añade un asset al inventario del usuario actual.
    Entrada:
      - asset_id: ID del asset a añadir
    Salida:
      - ok: True si se añadió
    """
    ok = State.usuario.add_asset(asset_id)
    return {"ok": ok, "owned_assets": State.usuario.owned_assets}

@rx.endpoint(method="POST")
def remove_asset_from_user(asset_id: str) -> dict:
    """
    Elimina un asset del inventario del usuario actual.
    Entrada:
      - asset_id: ID del asset a eliminar
    Salida:
      - ok: True si se eliminó
    """
    ok = State.usuario.remove_asset(asset_id)
    return {"ok": ok, "owned_assets": State.usuario.owned_assets}

@rx.endpoint(method="POST")
def set_user_status(estado: str) -> dict:
    """
    Cambia el estado del usuario (conectado, ausente, etc.).
    Entrada:
      - estado: nuevo estado
    Salida:
      - ok: True si se cambió
    """
    State.usuario.set_estado(estado)
    return {"ok": True, "estado": estado}

# --- FIN ENDPOINTS DE USUARIO --- 