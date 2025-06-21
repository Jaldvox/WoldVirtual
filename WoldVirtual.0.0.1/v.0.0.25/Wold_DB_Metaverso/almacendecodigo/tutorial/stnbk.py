import datetime  # Corregido el import de datatime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.DIFFICULTY_PREFIX = '000'
        self.pending_transactions = []
        self.create_block(proof=self._process_block(0), previous_hash='0')  # Bloque génesis

    def _process_block(self, previous_proof, is_validation=False):
        """Función unificada para procesar bloques: maneja prueba de trabajo y validación
        - Genera prueba de trabajo para nuevos bloques
        - Valida pruebas existentes
        - Imprime estado del proceso en terminal"""
        if is_validation:
            guess = str(previous_proof[0]**2 - previous_proof[1]**2).encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            print(f'Validando bloque - Hash: {guess_hash[:10]}...')
            return guess_hash[:3] == self.DIFFICULTY_PREFIX
        
        new_proof = 1
        while True:
            guess = str(new_proof**2 - previous_proof**2).encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            print(f'Minando bloque - Intento: {new_proof}, Hash: {guess_hash[:10]}...')
            if guess_hash[:3] == self.DIFFICULTY_PREFIX:
                print(f'¡Bloque minado exitosamente! Prueba: {new_proof}')
                return new_proof
            new_proof += 1

    def create_block(self, proof, previous_hash):
        """Crea y valida un nuevo bloque en la cadena
        - Maneja la creación de bloques
        - Realiza validaciones automáticas
        - Muestra resultados en terminal"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.pending_transactions.copy(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        
        if len(self.chain) > 0:
            print('\nValidando nuevo bloque...')
            if not self._process_block([proof, self.chain[-1]['proof']], True):
                print('Error: Bloque inválido - Prueba de trabajo incorrecta')
                raise ValueError("Bloque inválido")
            if previous_hash != self.hash(self.chain[-1]):
                print('Error: Bloque inválido - Hash anterior incorrecto')
                raise ValueError("Hash anterior inválido")
            print('Bloque validado correctamente')
        
        self.pending_transactions = []
        self.chain.append(block)
        print(f'Bloque #{block["index"]} añadido a la cadena\n')
        return block

    def hash(self, block):
        """Genera hash SHA-256 del bloque"""
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_transaction(self, sender, recipient, amount):
        """Añade nueva transacción y muestra confirmación"""
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        print(f'Nueva transacción añadida: {sender} -> {recipient}: {amount}')
        return len(self.chain) + 1

# Aplicación Flask
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    print('\nIniciando minería de nuevo bloque...')
    last_block = blockchain.chain[-1]
    proof = blockchain._process_block(last_block['proof'])
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        'message': 'Bloque minado exitosamente',
        'block': block
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    print('\nConsultando cadena de bloques...')
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    print('Iniciando blockchain...')
    app.run(host='0.0.0.0', port=5000)