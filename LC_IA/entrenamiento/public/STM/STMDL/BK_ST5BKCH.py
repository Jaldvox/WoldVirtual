import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    return hashlib.sha256(f"{index}{previous_hash}{timestamp}{data}".encode()).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Inicializar la blockchain con el bloque génesis
blockchain = [create_genesis_block()]

def add_block(data):
    """
    Añade un nuevo bloque con los datos proporcionados.
    """
    previous_block = blockchain[-1]
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)

def display_blockchain():
    """
    Muestra todos los bloques en la blockchain.
    """
    for block in blockchain:
        print(f"Bloque {block.index} - Hash: {block.hash}")
