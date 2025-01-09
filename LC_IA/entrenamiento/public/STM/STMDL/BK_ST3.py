# modulos/BK_ST3.py

import hashlib
from STMDL.BK_Usuarios import usuarios

def verificar_credenciales(username, password):
    """
    Verifica si las credenciales del usuario son correctas.
    Devuelve True si coinciden, False en caso contrario.
    """
    if username not in usuarios:
        print(f'Error: El usuario "{username}" no existe.')
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return usuarios[username] == hashed_password
