from typing import List
import datetime
import hashlib
from _1bk_inistn import Block
from block1 import Block  # Assuming your first module was named block1.py #

class Blockchain:
    def blockchain_manager(self, action='init', new_block=None, chain_check=False):
       
        # Initialize blockchain
        if action == 'init':
            self.chain: List[Block] = []
            self.difficulty = 2
            # Create genesis block
            genesis_block = Block(0, datetime.datetime.now(), "Genesis Block", "0")
            genesis_block.hash = genesis_block.calculate_hash()
            self.chain.append(genesis_block)
            return self.chain

        # Get latest block (helper function)
        latest_block = self.chain[-1] if self.chain else None

        # Add new block
        if action == 'add' and new_block:
            new_block.previous_hash = latest_block.hash
            new_block.mine_block(self.difficulty)
            self.chain.append(new_block)
            return new_block

        # Validate chain
        if chain_check:
            for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i-1]
                
                if (current_block.hash != current_block.calculate_hash() or
                    current_block.previous_hash != previous_block.hash):
                    return False
            return True

        return None

# Example usage
if __name__ == "__main__":
    my_blockchain = Blockchain()
    
    print("Mining block 1...")
    my_blockchain.add_block(Block(1, datetime.datetime.now(), {"amount": 10}))
    
    print("Mining block 2...")
    my_blockchain.add_block(Block(2, datetime.datetime.now(), {"amount": 20}))
    
    print("Blockchain valid?", my_blockchain.is_chain_valid())
    
    # Print the blockchain
    for block in my_blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")

        """
        Módulo Blockchain
        Este módulo implementa una estructura básica de blockchain con capacidades de minería y validación.
        La clase Blockchain proporciona un sistema de gestión de blockchain con las siguientes características:
        - Inicialización de blockchain con un bloque génesis
        - Adición de nuevos bloques con minería proof-of-work
        - Validación de cadena para asegurar integridad
        - Gestión de dificultad de minería de bloques

        El método blockchain_manager sirve como punto principal de control con tres modos:
        - 'init': Crea una nueva blockchain con bloque génesis
        - 'add': Añade un nuevo bloque a la cadena después de minarlo
        - chain_check: Valida la integridad de toda la blockchain

        Dependencias:
            - datetime: Para timestamps de bloques
            - hashlib: Para hash criptográfico
            - Clase Block desde block1.py: Para estructura de bloques

        Ejemplo:
            my_blockchain.blockchain_manager('init')  # Inicializar blockchain
            new_block = Block(1, datetime.datetime.now(), {"data": "transacción"})
            my_blockchain.blockchain_manager('add', new_block)  # Añadir nuevo bloque
            es_valido = my_blockchain.blockchain_manager(chain_check=True)  # Validar cadena

        Nota:
            El nivel de dificultad para minería está establecido en 2 por defecto
            Cada bloque debe ser minado antes de ser añadido a la cadena
            La blockchain mantiene integridad enlazando bloques mediante previous_hash.

        """
