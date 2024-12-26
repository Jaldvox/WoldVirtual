# BK_ST2_1.py - Funciones relacionadas con la blockchain
""""
import json
import hashlib
import datetime

# Función para calcular el hash de un bloque
def calcular_hash(bloque):
    bloque_str = f"{bloque['index']}{bloque['timestamp']}{bloque['data']}{bloque['prev_hash']}"
    return hashlib.sha256(bloque_str.encode()).hexdigest()

# Función para crear el bloque génesis
def crear_bloque_genesis():
    return {
        "index": 0,
        "timestamp": str(datetime.datetime.now()),
        "data": "Bloque génesis",
        "prev_hash": "0",
        "hash": " "
    }

# Función para guardar la blockchain en un archivo
def guardar_blockchain(blockchain, archivo="blockchain.json"):
    with open(archivo, "w") as f:
        json.dump(blockchain, f)

# Función para cargar la blockchain desde un archivo
def cargar_blockchain(archivo="blockchain.json"):
    try:
        with open(archivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [crear_bloque_genesis()]  # Si no existe, crea el bloque génesis.
