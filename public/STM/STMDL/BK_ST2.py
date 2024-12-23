import hashlib
from STMDL.BK_Usuarios import usuarios
from 

def registrar_usuario(username, password):
    """
    Registra un nuevo usuario con su contraseña.
    Devuelve True si el usuario fue registrado, False si ya existe.
    """
    if username in usuarios:
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    usuarios[username] = hashed_password
    return True
