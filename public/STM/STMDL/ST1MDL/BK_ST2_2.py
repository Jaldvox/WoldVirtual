# BK_ST2_2.py - Funciones para la creación y validación de bloques
""""
from BK_ST2_1 import calcular_hash, guardar_blockchain, cargar_blockchain

# Función para agregar un nuevo bloque a la cadena
def agregar_bloque(blockchain, datos):
    ultimo_bloque = blockchain[-1]
    nuevo_bloque = {
        "index": len(blockchain),
        "timestamp": str(datetime.datetime.now()),
        "data": datos,
        "prev_hash": ultimo_bloque["hash"],
        "hash": calcular_hash({
            "index": len(blockchain),
            "timestamp": str(datetime.datetime.now()),
            "data": datos,
            "prev_hash": ultimo_bloque["hash"]
        })
    }
    blockchain.append(nuevo_bloque)
    guardar_blockchain(blockchain)

# Función para verificar si la blockchain es válida
def verificar_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        bloque_actual = blockchain[i]
        bloque_anterior = blockchain[i - 1]

        if bloque_actual["prev_hash"] != bloque_anterior["hash"]:
            return False

        if calcular_hash(bloque_actual) != bloque_actual["hash"]:
            return False

    return True
