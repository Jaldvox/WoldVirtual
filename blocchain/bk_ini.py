import datetime
import hashlib
import json

class Blockchain:
    DIFFICULTY_PREFIX = '0000'

    def __init__(self):
        self.chain = []
        # Genesis block
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        """Devuelve el hash SHA-256 de un bloque."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, previous_proof):
        """Resuelve el problema de prueba de trabajo."""
        new_proof = 1
        while True:
            guess = f"{new_proof**2 - previous_proof**2}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash.startswith(self.DIFFICULTY_PREFIX):
                return new_proof
            new_proof += 1

    def mine_new_block(self):
        """Mina un nuevo bloque y lo añade a la cadena."""
        previous_block = self.chain[-1]
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        return self.create_block(proof, previous_hash)