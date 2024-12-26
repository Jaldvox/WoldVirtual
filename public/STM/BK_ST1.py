from STMDL.BK_ST2 import registrar_usuario
from STMDL.BK_ST3 import verificar_credenciales
from STMDL.BK_ST4 import manejar_accion
from STMDL.BK_Usuarios import inicializar_usuarios
from STMDL.BK_ST5BKCH import add_block, display_blockchain

def main():
    try:
        inicializar_usuarios()
        username = 'usuario1'
        password = 'contraseña_segura'
        if not username or not password:
            raise ValueError("El nombre de usuario y la contraseña no pueden estar vacíos.")
        if registrar_usuario(username, password):
            print(f'Usuario "{username}" registrado con éxito.')
        else:
            print(f'Error: El usuario "{username}" ya existe.')
        if verificar_credenciales(username, password):
            print(f'Credenciales verificadas con éxito para "{username}".')
        else:
            print(f'Error: Fallo al verificar credenciales para "{username}".')
            return  # Terminar ejecución si las credenciales fallan
        manejar_accion(username, "explorar")
        data = 'Datos del paquete de módulos'
        add_block(data)
        display_blockchain()
    except ValueError as ve:
        print(f'Error de validación: {ve}')
    except KeyError as ke:
        print(f'Error de clave: {ke}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

if __name__ == '__main__':
    main()