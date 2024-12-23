# modulo principal #

from BK_ST2 import registrar_usuario
from BK_ST3 import verificar_credenciales
from BK_ST4 import manejar_accion

if __name__ == '__main__':
    username = 'usuario1'
    password = 'contraseña_segura'
    registrar_usuario(username, password)
    print(f'Usuario {username} registrado con éxito.')

 if verificar_credenciales(username, password):
        print('Credenciales verificadas con éxito.')
    else:
        print('Error al verificar credenciales.')
        
    # Manejar acción
    manejar_accion(username, "explorar")
