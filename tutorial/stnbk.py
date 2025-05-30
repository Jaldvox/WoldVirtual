# import datatime
import hashlib
import json
import Flask

class Blockchain:
    def __init__(self):
        self.chain = []
        self.DIFFICULTY_PREFIX = '000'
        self.pending_transactions = []
        proof = self._create_proof(0)  # Genesis block
        self.create_block(proof=proof, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """Creates and validates a new block in the chain"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.pending_transactions.copy(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        
        if len(self.chain) > 0:
            if not self._validate_block(block, self.chain[-1]):
                raise ValueError("Invalid block")
        
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def _validate_block(self, new_block, previous_block):
        """Validates a block before adding it to the chain"""
        if new_block['previous_hash'] != self.hash(previous_block):
            return False
        if not self._is_valid_proof(new_block['proof'], previous_block['proof']):
            return False
        return True

    def _create_proof(self, previous_proof):
        """Creates proof of work"""
        new_proof = 1
        while not self._is_valid_proof(new_proof, previous_proof):
            new_proof += 1
        return new_proof

    def _is_valid_proof(self, new_proof, previous_proof):
        """Checks if a proof is valid"""
        guess = str(new_proof**2 - previous_proof**2).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == self.DIFFICULTY_PREFIX

    def hash(self, block):
        """Creates SHA-256 hash of a block"""
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_transaction(self, sender, recipient, amount):
        """Adds a new transaction to pending transactions"""
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.get_last_block()['index'] + 1

    def get_last_block(self):
        """Returns the last block in the chain"""
        return self.chain[-1]

# Flask application
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    proof = blockchain._create_proof(last_block['proof'])
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        'message': 'Block mined successfully',
        'block': block
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200
    
    
    """
    Implementación Básica de Blockchain en Python (Actualizado: 30/05/2025 20:39)

    Funciones Principales:
    1. __init__(): Inicializa blockchain con bloque génesis y establece dificultad de minería
    2. create_block(): Crea y valida nuevos bloques con transacciones pendientes 
    3. _validate_block(): Asegura la integridad del bloque y prueba de trabajo válida
    4. _create_proof(): Genera prueba de trabajo para nuevos bloques
    5. _is_valid_proof(): Valida que la prueba de trabajo cumpla el requisito de dificultad
    6. hash(): Genera hash SHA-256 para los bloques
    7. add_transaction(): Añade nuevas transacciones al pool pendiente
    8. get_last_block(): Recupera el bloque más reciente

    Endpoints API:
    - /mine_block: Mina nuevo bloque con transacciones pendientes
    - /get_chain: Devuelve el estado actual de la blockchain

    Detalles Técnicos:
    - Dificultad de minería: requiere prefijo '000'  
    - Prueba de Trabajo: Basada en hash de diferencia de cuadrados
    - Estructura del bloque: índice, marca temporal, transacciones, prueba, hash anterior

    Problemas Conocidos:
    - Importación datetime necesita corrección (actualmente 'datatime')
    - Se necesita validación adicional de la cadena.
    
    """