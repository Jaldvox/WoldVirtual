# BK_ST2_1.py - Funciones relacionadas con la blockchain
import json
import hashlib
import datetime

# Función para calcular el hash de un bloque
def calcular_hash(bloque):
    bloque_str = f"{bloque['index']}{bloque['timestamp']}{bloque['data']}{bloque['prev_hash']}"
    return hashlib.sha256(bloque_str.encode()).hexdigest()

# Función para crear el bloque génesis
def crear_bloque_genesis():
    bloque_genesis = {
        "index": 0,
        "timestamp": str(datetime.datetime.now()),
        "data": "Bloque génesis",
        "prev_hash": "0",
    }
    bloque_genesis["hash"] = calcular_hash(bloque_genesis)
    return bloque_genesis

# Función para validar la blockchain
def validar_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        bloque_actual = blockchain[i]
        bloque_anterior = blockchain[i - 1]
        if bloque_actual["hash"] != calcular_hash(bloque_actual) or bloque_actual["prev_hash"] != bloque_anterior["hash"]:
            return False
    return True

# Función para añadir un nuevo bloque a la blockchain con validación
def añadir_bloque(blockchain, data):
    if not validar_blockchain(blockchain):
        raise ValueError("La blockchain no es válida")
    
    ultimo_bloque = blockchain[-1]
    nuevo_bloque = {
        "index": ultimo_bloque["index"] + 1,
        "timestamp": str(datetime.datetime.now()),
        "data": data,
        "prev_hash": ultimo_bloque["hash"],
    }
    nuevo_bloque["hash"] = calcular_hash(nuevo_bloque)
    blockchain.append(nuevo_bloque)
    return nuevo_bloque

# Función para guardar la blockchain en un archivo
def guardar_blockchain(blockchain, archivo="blockchain.json"):
    with open(archivo, "w") as f:
        json.dump(blockchain, f, indent=4)

# Función para cargar la blockchain desde un archivo
def cargar_blockchain(archivo="blockchain.json"):
    try:
        with open(archivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [crear_bloque_genesis()]  # Si no existe, crea el bloque génesis
    except json.JSONDecodeError:
        raise ValueError("El archivo de la blockchain está corrupto")
