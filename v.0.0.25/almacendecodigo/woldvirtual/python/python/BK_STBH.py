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
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Crear la blockchain y agregar el bloque génesis
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Agregar 11 bloques a la blockchain
for i in range(1, 12):
    block_data = f"Bloque {i}"
    new_block = create_new_block(previous_block, block_data)
    blockchain.append(new_block)
    previous_block = new_block

# Mostrar la blockchain
for block in blockchain:
    print(f"Índice: {block.index}")
    print(f"Hash anterior: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}\n")
