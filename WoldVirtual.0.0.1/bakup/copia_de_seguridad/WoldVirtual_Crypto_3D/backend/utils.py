"""Utilidades para el backend."""
import jwt
from datetime import datetime, timedelta
from typing import Optional
import ipfshttpclient
from web3 import Web3
import os

from .config import settings

# Utilidades de autenticación
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear un token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str):
    """Verificar un token JWT."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None

# Utilidades de IPFS
def upload_to_ipfs(file_path: str) -> str:
    """Subir un archivo a IPFS."""
    client = ipfshttpclient.connect(settings.IPFS_API_URL)
    result = client.add(file_path)
    return result["Hash"]

def get_ipfs_url(hash: str) -> str:
    """Obtener la URL de un archivo en IPFS."""
    return f"https://ipfs.io/ipfs/{hash}"

# Utilidades de Web3
def get_web3():
    """Obtener una instancia de Web3."""
    return Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))

def verify_wallet_signature(message: str, signature: str, address: str) -> bool:
    """Verificar la firma de una billetera."""
    w3 = get_web3()
    try:
        recovered_address = w3.eth.account.recover_message(
            message,
            signature=signature
        )
        return recovered_address.lower() == address.lower()
    except Exception:
        return False

# Utilidades de archivos
def save_upload_file(upload_file, folder: str = None) -> str:
    """Guardar un archivo subido."""
    if folder is None:
        folder = settings.UPLOAD_FOLDER
    
    # Crear el directorio si no existe
    os.makedirs(folder, exist_ok=True)
    
    # Generar un nombre de archivo único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{upload_file.filename}"
    file_path = os.path.join(folder, filename)
    
    # Guardar el archivo
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    
    return file_path

def delete_file(file_path: str):
    """Eliminar un archivo."""
    if os.path.exists(file_path):
        os.remove(file_path)

# Utilidades de validación
def validate_file_type(filename: str, allowed_extensions: set) -> bool:
    """Validar el tipo de archivo."""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in allowed_extensions

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validar el tamaño del archivo."""
    return file_size <= max_size 