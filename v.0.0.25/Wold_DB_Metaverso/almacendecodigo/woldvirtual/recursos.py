import hashlib
# Importamos la clase Blockchain
from blockchain import Blockchain

# Ya no necesitamos el diccionario global de usuarios
# usuarios = {}

def registrar_usuario(blockchain: Blockchain, username, password):
    # En un sistema real, verificaríamos si el usuario ya existe en la blockchain
    # Para este ejemplo simplificado, simplemente añadimos la transacción de registro
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Creamos una transacción de registro de usuario
    transaccion_registro = {
        'type': 'registro_usuario',
        'username': username,
        'hashed_password': hashed_password,
        'timestamp': time.time() # Añadimos un timestamp a la transacción
    }
    # Añadimos la transacción a la lista de transacciones pendientes de la blockchain
    blockchain.pending_transactions.append(transaccion_registro)
    print(f"Transacción de registro para el usuario {username} añadida a la cola.")
    print("Se minará en el próximo bloque.") # Indicamos que se procesará después

def verificar_credenciales(blockchain: Blockchain, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Para verificar, buscamos la última transacción de registro para este usuario en la cadena
    # Esto es una simplificación; en una blockchain real, la verificación sería más compleja
    latest_registration = None
    for block in blockchain.chain:
        # Asumimos que los datos del bloque son una lista de transacciones
        if isinstance(block.get('data'), list):
            for transaction in block['data']:
                if transaction.get('type') == 'registro_usuario' and transaction.get('username') == username:
                    latest_registration = transaction

    # También buscamos en las transacciones pendientes
    for transaction in blockchain.pending_transactions:
         if transaction.get('type') == 'registro_usuario' and transaction.get('username') == username:
                    latest_registration = transaction


    if latest_registration and latest_registration.get('hashed_password') == hashed_password:
        return True
    else:
        return False

def manejar_accion(usuario, accion):
    if accion == "explorar":
        print(f"Bienvenido/a {usuario} al entorno de exploración.")
    elif accion == "intercambiar":
        print(f"Realizando intercambio para {usuario}.")
    else:
        print("Acción no reconocida.")

# Importamos time para usarlo en la transacción de registro
import time
# Importamos la clase Blockchain (aunque ya no se usa directamente aquí, la mantenemos por si las clases de recursos la necesitan en el futuro)
from blockchain import Blockchain
import time # Importamos time por si las clases de recursos lo necesitan

# Eliminamos las funciones de usuario que ahora están en usuarios.py
# def registrar_usuario(blockchain: Blockchain, username, password):
#     ...
# def verificar_credenciales(blockchain: Blockchain, username, password):
#     ...
# def manejar_accion(usuario, accion):
#     ...

class RecursosUsuario:
    def __init__(self, porcentaje_cpu, porcentaje_ancho_banda):
        self.porcentaje_cpu = porcentaje_cpu
        self.porcentaje_ancho_banda = porcentaje_ancho_banda

    @staticmethod
    def asignar_recursos_a_usuario(usuario, recursos_comunitarios):
        recursos_asignados = {
            'cpu': recursos_comunitarios['cpu'] * (usuario.porcentaje_cpu / 100),
            'ancho_banda': recursos_comunitarios['ancho_banda'] * (usuario.porcentaje_ancho_banda / 100),
        }
        return recursos_asignados

class MonitoreoRecursos:
    def __init__(self):
        self.recursos_usuarios = {}

    def actualizar_recursos(self, nombre_usuario, uso_cpu, uso_ancho_banda):
        self.recursos_usuarios[nombre_usuario] = {
            'uso_cpu': uso_cpu,
            'uso_ancho_banda': uso_ancho_banda
        }

    def obtener_informacion(self):
        return self.recursos_usuarios

    @staticmethod
    def inicializar():
        print("Recursos inicializados")
# Importamos la clase Blockchain (aunque ya no se usa directamente aquí, la mantenemos por si las clases de recursos la necesitan en el futuro)
from blockchain import Blockchain
import time # Importamos time por si las clases de recursos lo necesitan

# Eliminamos las funciones de usuario que ahora están en usuarios.py
# def registrar_usuario(blockchain: Blockchain, username, password):
#     ...
# def verificar_credenciales(blockchain: Blockchain, username, password):
#     ...
# def manejar_accion(usuario, accion):
#     ...

class RecursosUsuario:
    def __init__(self, porcentaje_cpu, porcentaje_ancho_banda):
        self.porcentaje_cpu = porcentaje_cpu
        self.porcentaje_ancho_banda = porcentaje_ancho_banda

    @staticmethod
    def asignar_recursos_a_usuario(usuario, recursos_comunitarios):
        recursos_asignados = {
            'cpu': recursos_comunitarios['cpu'] * (usuario.porcentaje_cpu / 100),
            'ancho_banda': recursos_comunitarios['ancho_banda'] * (usuario.porcentaje_ancho_banda / 100),
        }
        return recursos_asignados

class MonitoreoRecursos:
    def __init__(self):
        self.recursos_usuarios = {}

    def actualizar_recursos(self, nombre_usuario, uso_cpu, uso_ancho_banda):
        self.recursos_usuarios[nombre_usuario] = {
            'uso_cpu': uso_cpu,
            'uso_ancho_banda': uso_ancho_banda
        }

    def obtener_informacion(self):
        return self.recursos_usuarios

    @staticmethod
    def inicializar():
        print("Recursos inicializados")
class RecursosUsuario:
    def __init__(self, porcentaje_cpu, porcentaje_ancho_banda):
        self.porcentaje_cpu = porcentaje_cpu
        self.porcentaje_ancho_banda = porcentaje_ancho_banda

    @staticmethod
    def asignar_recursos_a_usuario(usuario, recursos_comunitarios):
        recursos_asignados = {
            'cpu': recursos_comunitarios['cpu'] * (usuario.porcentaje_cpu / 100),
            'ancho_banda': recursos_comunitarios['ancho_banda'] * (usuario.porcentaje_ancho_banda / 100),
        }
        return recursos_asignados

class MonitoreoRecursos:
    def __init__(self):
        self.recursos_usuarios = {}

    def actualizar_recursos(self, nombre_usuario, uso_cpu, uso_ancho_banda):
        self.recursos_usuarios[nombre_usuario] = {
            'uso_cpu': uso_cpu,
            'uso_ancho_banda': uso_ancho_banda
        }

    def obtener_informacion(self):
        return self.recursos_usuarios

    @staticmethod
    def inicializar():
        print("Recursos inicializados")
