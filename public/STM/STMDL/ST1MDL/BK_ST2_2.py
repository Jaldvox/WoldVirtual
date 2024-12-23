import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def to_dict(self):
        """Convierte el bloque en un diccionario para su representación JSON."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        """Inicializa la blockchain con el bloque génesis."""
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Crea el bloque génesis de la blockchain."""
        return Block(
            0, 
            "0", 
            int(time.time()), 
            "Genesis Block", 
            self.calculate_hash(0, "0", int(time.time()), "Genesis Block")
        )

    def calculate_hash(self, index, previous_hash, timestamp, data):
        """Calcula el hash de un bloque."""
        return hashlib.sha256(f"{index}{previous_hash}{timestamp}{data}".encode()).hexdigest()

    def create_new_block(self, previous_block, data):
        """Crea un nuevo bloque basado en el bloque anterior."""
        index = previous_block.index + 1
        timestamp = int(time.time())
        hash = self.calculate_hash(index, previous_block.hash, timestamp, data)
        return Block(index, previous_block.hash, timestamp, data, hash)

    def add_block(self, data, previous_hash):
        """Añade un nuevo bloque a la cadena."""
        previous_block = self.chain[-1]

        # Validar el hash anterior proporcionado
        if previous_hash != previous_block.hash:
            raise ValueError("El hash anterior no coincide con el último bloque de la cadena.")

        # Crear y añadir el nuevo bloque
        new_block = self.create_new_block(previous_block, data)
        self.chain.append(new_block)
        return new_block.to_dict()
