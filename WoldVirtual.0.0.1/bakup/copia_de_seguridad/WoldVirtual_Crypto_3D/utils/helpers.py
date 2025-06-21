"""
Funciones helper y utilidades generales para WoldVirtual Crypto 3D
Contiene funciones de utilidad, formateo, conversiones y validaciones.
"""

import re
import hashlib
import uuid
import json
import base64
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union, Tuple
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# FUNCIONES DE VALIDACIÓN
# =============================================================================

def validate_email(email: str) -> bool:
    """
    Valida el formato de un email.
    
    Args:
        email: Email a validar
        
    Returns:
        bool: True si el email es válido, False en caso contrario
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_wallet_address(address: str) -> bool:
    """
    Valida una dirección de wallet Ethereum.
    
    Args:
        address: Dirección de wallet a validar
        
    Returns:
        bool: True si la dirección es válida, False en caso contrario
    """
    if not address:
        return False
    
    # Verificar formato básico
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    
    # Verificar checksum (opcional, pero recomendado)
    try:
        # Convertir a checksum address
        checksum_address = address.lower()
        if address != checksum_address:
            return False
    except Exception:
        return False
    
    return True

def validate_username(username: str) -> bool:
    """
    Valida un nombre de usuario.
    
    Args:
        username: Nombre de usuario a validar
        
    Returns:
        bool: True si el username es válido, False en caso contrario
    """
    if not username:
        return False
    
    # Longitud entre 3 y 20 caracteres
    if len(username) < 3 or len(username) > 20:
        return False
    
    # Solo letras, números, guiones bajos y guiones medios
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, username))

def validate_password(password: str) -> Tuple[bool, List[str]]:
    """
    Valida una contraseña y retorna errores específicos.
    
    Args:
        password: Contraseña a validar
        
    Returns:
        Tuple[bool, List[str]]: (es_válida, lista_de_errores)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        errors.append("La contraseña debe contener al menos una mayúscula")
    
    if not re.search(r'[a-z]', password):
        errors.append("La contraseña debe contener al menos una minúscula")
    
    if not re.search(r'\d', password):
        errors.append("La contraseña debe contener al menos un número")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("La contraseña debe contener al menos un carácter especial")
    
    return len(errors) == 0, errors

def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Valida el tipo de archivo basado en su extensión.
    
    Args:
        filename: Nombre del archivo
        allowed_extensions: Lista de extensiones permitidas
        
    Returns:
        bool: True si el tipo de archivo es válido
    """
    if not filename:
        return False
    
    file_extension = get_file_extension(filename).lower()
    return file_extension in [ext.lower() for ext in allowed_extensions]

def validate_file_size(file_size: int, max_size: int) -> bool:
    """
    Valida el tamaño de un archivo.
    
    Args:
        file_size: Tamaño del archivo en bytes
        max_size: Tamaño máximo permitido en bytes
        
    Returns:
        bool: True si el tamaño es válido
    """
    return file_size <= max_size

# =============================================================================
# FUNCIONES DE FORMATEO
# =============================================================================

def format_address(address: str, start_chars: int = 6, end_chars: int = 4) -> str:
    """
    Formatea una dirección de wallet para mostrar.
    
    Args:
        address: Dirección completa
        start_chars: Número de caracteres al inicio
        end_chars: Número de caracteres al final
        
    Returns:
        str: Dirección formateada (ej: 0x1234...5678)
    """
    if not address or len(address) < start_chars + end_chars:
        return address
    
    return f"{address[:start_chars]}...{address[-end_chars:]}"

def format_balance(balance: Union[int, float, str], decimals: int = 18) -> str:
    """
    Formatea un balance de tokens.
    
    Args:
        balance: Balance en wei o unidades más pequeñas
        decimals: Número de decimales del token
        
    Returns:
        str: Balance formateado
    """
    try:
        if isinstance(balance, str):
            balance = int(balance)
        
        # Convertir de wei a ETH
        eth_balance = balance / (10 ** decimals)
        
        # Formatear con 4 decimales máximo
        if eth_balance >= 1:
            return f"{eth_balance:.4f}"
        elif eth_balance >= 0.0001:
            return f"{eth_balance:.6f}"
        else:
            return f"{eth_balance:.8f}"
    except (ValueError, TypeError):
        return "0.0000"

def format_file_size(size_bytes: int) -> str:
    """
    Formatea el tamaño de archivo en bytes a formato legible.
    
    Args:
        size_bytes: Tamaño en bytes
        
    Returns:
        str: Tamaño formateado (ej: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_timestamp(timestamp: Union[int, float, datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formatea un timestamp a string legible.
    
    Args:
        timestamp: Timestamp a formatear
        format_str: Formato de salida
        
    Returns:
        str: Timestamp formateado
    """
    if isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    elif isinstance(timestamp, datetime):
        dt = timestamp
    else:
        return str(timestamp)
    
    return dt.strftime(format_str)

def format_duration(seconds: int) -> str:
    """
    Formatea una duración en segundos a formato legible.
    
    Args:
        seconds: Duración en segundos
        
    Returns:
        str: Duración formateada (ej: "2h 30m 15s")
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours}h {remaining_minutes}m {remaining_seconds}s"

# =============================================================================
# FUNCIONES DE CONVERSIÓN
# =============================================================================

def wei_to_eth(wei_amount: Union[int, str]) -> float:
    """
    Convierte wei a ETH.
    
    Args:
        wei_amount: Cantidad en wei
        
    Returns:
        float: Cantidad en ETH
    """
    try:
        if isinstance(wei_amount, str):
            wei_amount = int(wei_amount)
        return wei_amount / (10 ** 18)
    except (ValueError, TypeError):
        return 0.0

def eth_to_wei(eth_amount: Union[float, str]) -> int:
    """
    Convierte ETH a wei.
    
    Args:
        eth_amount: Cantidad en ETH
        
    Returns:
        int: Cantidad en wei
    """
    try:
        if isinstance(eth_amount, str):
            eth_amount = float(eth_amount)
        return int(eth_amount * (10 ** 18))
    except (ValueError, TypeError):
        return 0

def hex_to_int(hex_string: str) -> int:
    """
    Convierte un string hexadecimal a entero.
    
    Args:
        hex_string: String hexadecimal
        
    Returns:
        int: Valor entero
    """
    try:
        return int(hex_string, 16)
    except (ValueError, TypeError):
        return 0

def int_to_hex(value: int, prefix: bool = True) -> str:
    """
    Convierte un entero a string hexadecimal.
    
    Args:
        value: Valor entero
        prefix: Si incluir el prefijo "0x"
        
    Returns:
        str: String hexadecimal
    """
    hex_str = hex(value)[2:]  # Remover "0x"
    if prefix:
        return f"0x{hex_str}"
    return hex_str

def bytes_to_hex(data: bytes) -> str:
    """
    Convierte bytes a string hexadecimal.
    
    Args:
        data: Datos en bytes
        
    Returns:
        str: String hexadecimal
    """
    return data.hex()

def hex_to_bytes(hex_string: str) -> bytes:
    """
    Convierte string hexadecimal a bytes.
    
    Args:
        hex_string: String hexadecimal
        
    Returns:
        bytes: Datos en bytes
    """
    return bytes.fromhex(hex_string.replace('0x', ''))

# =============================================================================
# FUNCIONES DE ARCHIVO
# =============================================================================

def get_file_extension(filename: str) -> str:
    """
    Obtiene la extensión de un archivo.
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        str: Extensión del archivo (sin el punto)
    """
    if not filename:
        return ""
    
    parts = filename.split('.')
    if len(parts) > 1:
        return parts[-1].lower()
    return ""

def get_file_name_without_extension(filename: str) -> str:
    """
    Obtiene el nombre del archivo sin extensión.
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        str: Nombre sin extensión
    """
    if not filename:
        return ""
    
    parts = filename.split('.')
    if len(parts) > 1:
        return '.'.join(parts[:-1])
    return filename

def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    """
    Genera un nombre de archivo único.
    
    Args:
        original_filename: Nombre original del archivo
        prefix: Prefijo opcional
        
    Returns:
        str: Nombre único generado
    """
    extension = get_file_extension(original_filename)
    name_without_ext = get_file_name_without_extension(original_filename)
    unique_id = str(uuid.uuid4())[:8]
    
    if prefix:
        return f"{prefix}_{name_without_ext}_{unique_id}.{extension}"
    return f"{name_without_ext}_{unique_id}.{extension}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo removiendo caracteres peligrosos.
    
    Args:
        filename: Nombre del archivo a sanitizar
        
    Returns:
        str: Nombre sanitizado
    """
    if not filename:
        return ""
    
    # Remover caracteres peligrosos
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remover espacios múltiples
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Remover espacios al inicio y final
    sanitized = sanitized.strip()
    
    return sanitized

# =============================================================================
# FUNCIONES DE HASH Y ENCRIPTACIÓN
# =============================================================================

def generate_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Genera un hash de los datos proporcionados.
    
    Args:
        data: Datos a hashear
        algorithm: Algoritmo de hash a usar
        
    Returns:
        str: Hash generado
    """
    if algorithm == "md5":
        return hashlib.md5(data.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(data.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(data.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(data.encode()).hexdigest()
    else:
        raise ValueError(f"Algoritmo de hash no soportado: {algorithm}")

def generate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Genera un hash de un archivo.
    
    Args:
        file_path: Ruta del archivo
        algorithm: Algoritmo de hash a usar
        
    Returns:
        str: Hash del archivo
    """
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {file_path}")
        return ""
    except Exception as e:
        logger.error(f"Error al generar hash del archivo: {e}")
        return ""

def generate_random_string(length: int = 32) -> str:
    """
    Genera una cadena aleatoria.
    
    Args:
        length: Longitud de la cadena
        
    Returns:
        str: Cadena aleatoria
    """
    import secrets
    import string
    
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# =============================================================================
# FUNCIONES DE JSON
# =============================================================================

def safe_json_loads(data: str, default: Any = None) -> Any:
    """
    Carga JSON de forma segura.
    
    Args:
        data: String JSON
        default: Valor por defecto si falla
        
    Returns:
        Any: Datos parseados o valor por defecto
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """
    Convierte datos a JSON de forma segura.
    
    Args:
        data: Datos a convertir
        default: String por defecto si falla
        
    Returns:
        str: String JSON o valor por defecto
    """
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError):
        return default

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Combina dos diccionarios de forma profunda.
    
    Args:
        dict1: Primer diccionario
        dict2: Segundo diccionario
        
    Returns:
        Dict: Diccionario combinado
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result

# =============================================================================
# FUNCIONES DE VALIDACIÓN DE DATOS
# =============================================================================

def is_valid_json(data: str) -> bool:
    """
    Verifica si un string es JSON válido.
    
    Args:
        data: String a verificar
        
    Returns:
        bool: True si es JSON válido
    """
    try:
        json.loads(data)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

def is_valid_url(url: str) -> bool:
    """
    Verifica si una URL es válida.
    
    Args:
        url: URL a verificar
        
    Returns:
        bool: True si la URL es válida
    """
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return bool(re.match(pattern, url))

def is_valid_ip_address(ip: str) -> bool:
    """
    Verifica si una dirección IP es válida.
    
    Args:
        ip: Dirección IP a verificar
        
    Returns:
        bool: True si la IP es válida
    """
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

# =============================================================================
# FUNCIONES DE LIMPIEZA DE DATOS
# =============================================================================

def clean_string(text: str) -> str:
    """
    Limpia un string removiendo caracteres especiales y espacios extra.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    if not text:
        return ""
    
    # Remover caracteres de control
    text = ''.join(char for char in text if ord(char) >= 32)
    
    # Remover espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    # Remover espacios al inicio y final
    return text.strip()

def remove_html_tags(html: str) -> str:
    """
    Remueve tags HTML de un string.
    
    Args:
        html: String con HTML
        
    Returns:
        str: String sin HTML
    """
    pattern = r'<[^>]+>'
    return re.sub(pattern, '', html)

def normalize_whitespace(text: str) -> str:
    """
    Normaliza espacios en blanco en un texto.
    
    Args:
        text: Texto a normalizar
        
    Returns:
        str: Texto con espacios normalizados
    """
    if not text:
        return ""
    
    # Reemplazar múltiples espacios con uno solo
    text = re.sub(r'\s+', ' ', text)
    
    # Remover espacios al inicio y final
    return text.strip()

# =============================================================================
# FUNCIONES DE UTILIDAD GENERAL
# =============================================================================

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Divide una lista en chunks del tamaño especificado.
    
    Args:
        lst: Lista a dividir
        chunk_size: Tamaño de cada chunk
        
    Returns:
        List[List[Any]]: Lista de chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def flatten_list(nested_list: List[Any]) -> List[Any]:
    """
    Aplana una lista anidada.
    
    Args:
        nested_list: Lista anidada
        
    Returns:
        List[Any]: Lista aplanada
    """
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

def remove_duplicates(lst: List[Any]) -> List[Any]:
    """
    Remueve duplicados de una lista manteniendo el orden.
    
    Args:
        lst: Lista con posibles duplicados
        
    Returns:
        List[Any]: Lista sin duplicados
    """
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def get_nested_value(data: Dict, keys: List[str], default: Any = None) -> Any:
    """
    Obtiene un valor anidado de un diccionario.
    
    Args:
        data: Diccionario de datos
        keys: Lista de claves para navegar
        default: Valor por defecto si no se encuentra
        
    Returns:
        Any: Valor encontrado o valor por defecto
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def set_nested_value(data: Dict, keys: List[str], value: Any) -> bool:
    """
    Establece un valor anidado en un diccionario.
    
    Args:
        data: Diccionario de datos
        keys: Lista de claves para navegar
        value: Valor a establecer
        
    Returns:
        bool: True si se estableció correctamente
    """
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    return True 