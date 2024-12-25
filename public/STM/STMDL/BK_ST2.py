import hashlib
from STMDL.BK_Usuarios import usuarios
from BK_ST2_2 import agregar_bloque
from BK_ST2_3 import sincronizar_blockchain
from BK_ST2_4 import iniciar_servidor
from BK_ST2_1 import cargar_blockchain, guardar_blockchain, crear_bloque_genesis

def iniciar_red():
    """
    Esta función se encarga de iniciar el nodo y sincronizarlo con otros nodos.
    Primero sincroniza la blockchain y luego inicia el servidor.
    """
    print("Iniciando la sincronización de la blockchain con otros nodos...")
    
    # Sincronizar la blockchain con otros nodos
    blockchain = sincronizar_blockchain()
    
    # Verificar si la blockchain local está vacía o si solo tiene el bloque génesis
    if len(blockchain) == 1:  # Solo contiene el bloque génesis
        print("Blockchain vacía. Creando el bloque génesis...")
        blockchain = [crear_bloque_genesis()]  # Crear el bloque génesis si no existe
    
    # Guardar la blockchain sincronizada
    guardar_blockchain(blockchain)
    print(f"Blockchain sincronizada y guardada. Total de bloques: {len(blockchain)}")

    # Iniciar el servidor del nodo
    print("Iniciando el servidor del nodo...")
    iniciar_servidor()

def agregar_bloque_a_la_red(datos):
    """
    Esta función permite agregar un nuevo bloque a la blockchain.
    Recibe los datos del bloque, lo crea y lo agrega a la blockchain.
    """
    blockchain = cargar_blockchain()
    print("Agregando un nuevo bloque a la blockchain...")
    
    # Agregar un nuevo bloque
    agregar_bloque(blockchain, datos)
    
    # Guardar la blockchain actualizada
    guardar_blockchain(blockchain)
    print(f"Nuevo bloque agregado con datos: {datos}")
    print(f"Blockchain actualizada. Total de bloques: {len(blockchain)}")

if __name__ == "__main__":
    """
    El archivo principal. Aquí puedes elegir qué funcionalidad deseas ejecutar.
    """
    # Llamada para iniciar la red de nodos
    iniciar_red()

    # Si deseas agregar bloques manualmente:
    # Puedes descomentar la siguiente línea para agregar un bloque con datos personalizados.
    # agregar_bloque_a_la_red("Este es un nuevo bloque con información.")


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
