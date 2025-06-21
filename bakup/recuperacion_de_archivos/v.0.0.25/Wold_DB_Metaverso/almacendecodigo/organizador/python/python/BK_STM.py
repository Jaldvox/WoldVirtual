import hashlib
import time

class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.size = len(str(self.__dict__).encode('utf-8'))  # Calcula el tamaño del bloque en bytes

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') + 
                    str(self.data).encode('utf-8') + 
                    str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(time.time(), "Bloque Génesis", "0")

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def get_size(self):
        total_size = 0
        for block in self.chain:
            total_size += block.size
        return total_size

# Crear la blockchain
blockchain = Blockchain()

# Generar 30 bloques
for i in range(30):
    data = f"Datos del bloque {i+1}"
    blockchain.add_block(Block(time.time(), data, blockchain.chain[-1].hash))

# Mostrar información de la blockchain
print("Blockchain creada:")
for block in blockchain.chain:
    print(f"  Timestamp: {block.timestamp}")
    print(f"  Datos: {block.data}")
    print(f"  Hash: {block.hash}")
    print(f"  Tamaño: {block.size} bytes")
    print(f"  Hash previo: {block.previous_hash}")
    print("-" * 50)

print(f"Tamaño total de la blockchain: {blockchain.get_size()} bytes")
