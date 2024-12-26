from STMDL.BK_ST2 import registrar_usuario
from STMDL.BK_ST3 import verificar_credenciales
from STMDL.BK_ST4 import manejar_accion
from STMDL.BK_Usuarios import inicializar_usuarios
from STMDL.BK_ST5BKCH  import add_block, display_blockchain

# Copia de seguridad y recuperación de recursos que funcionan. #

if __name__ == '__main__':
    # Datos de prueba para la blockchain
    data = 'Datos del paquete de módulos'
    add_block(data)

    # Mostrar la blockchain
    display_blockchain()

if __name__ == '__main__':
    # Inicializar sistema de usuarios
    inicializar_usuarios()

    # Datos del usuario
    username = 'usuario1'
    password = 'contraseña_segura'

    # Registrar usuario
    if registrar_usuario(username, password):
        print(f'Usuario "{username}" registrado con éxito.')
    else:
        print(f'Error: El usuario "{username}" ya existe.')

    # Verificar credenciales
    if verificar_credenciales(username, password):
        print(f'Credenciales verificadas con éxito para "{username}".')
    else:
        print(f'Error: Fallo al verificar credenciales para "{username}".')

    # Manejar acción
    manejar_accion(username, "explorar")