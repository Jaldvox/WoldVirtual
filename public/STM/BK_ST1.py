# modulo principal #

from BK_ST2 import registrar_usuario
from BK_ST3 import verificar_credenciales
from BK_ST3 import manejar_accion

# Ejemplo de uso de registrar_usuario
if __name__ == '__main__':
    username = 'usuario1'
    password = 'contraseña_segura'
    registrar_usuario(username, password)
    print(f'Usuario {username} registrado con éxito.')

