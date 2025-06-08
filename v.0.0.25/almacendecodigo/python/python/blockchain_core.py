import datetime
import hashlib
import json
from typing import List, Dict, Optional, Any
from flask import Flask, jsonify

class Block:
    def __init__(self, index: int, timestamp: str, transactions: List[Dict], proof: int, previous_hash: str):
        """
        Inicializa un nuevo bloque en la cadena.
        
        Args:
            index: El número del bloque en la cadena
            timestamp: La marca de tiempo de cuando se creó el bloque
            transactions: Lista de transacciones incluidas en el bloque
            proof: El número de prueba de trabajo
            previous_hash: El hash del bloque anterior
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calcula el hash del bloque usando sus atributos.
        
        Returns:
            str: El hash SHA256 del bloque
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> Dict:
        """
        Convierte el bloque a un diccionario.
        
        Returns:
            Dict: Representación del bloque en formato diccionario
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self):
        """
        Inicializa una nueva blockchain con un bloque génesis.
        """
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = 4  # Número de ceros iniciales requeridos para el hash
        self.mining_reward = 10  # Recompensa por minar un bloque
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        Crea y añade el bloque génesis a la cadena.
        """
        genesis_block = Block(
            index=0,
            timestamp=str(datetime.datetime.now()),
            transactions=[],
            proof=1,
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        """
        Obtiene el último bloque de la cadena.
        
        Returns:
            Block: El último bloque en la cadena
        """
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        Añade una nueva transacción al listado de transacciones pendientes.
        
        Args:
            sender: Dirección del remitente
            recipient: Dirección del destinatario
            amount: Cantidad a transferir
            
        Returns:
            int: Índice del bloque que contendrá esta transacción
        """
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': str(datetime.datetime.now())
        })
        return self.get_last_block().index + 1

    def proof_of_work(self, previous_proof: int) -> int:
        """
        Implementa el algoritmo de prueba de trabajo.
        
        Args:
            previous_proof: El proof del bloque anterior
            
        Returns:
            int: El nuevo proof que resuelve el problema
        """
        new_proof = 0
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(
                f'{new_proof**2 - previous_proof**2}'.encode()
            ).hexdigest()
            
            if hash_operation[:self.difficulty] == '0' * self.difficulty:
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def mine_block(self, miner_address: str) -> Block:
        """
        Mina un nuevo bloque procesando las transacciones pendientes.
        
        Args:
            miner_address: La dirección donde se enviará la recompensa por minado
            
        Returns:
            Block: El nuevo bloque minado
        """
        # Añadir la recompensa por minado a las transacciones pendientes
        self.add_transaction(
            sender="0",  # 0 representa nuevas monedas minadas
            recipient=miner_address,
            amount=self.mining_reward
        )

        # Obtener el último bloque
        previous_block = self.get_last_block()
        new_proof = self.proof_of_work(previous_block.proof)

        # Crear el nuevo bloque
        new_block = Block(
            index=len(self.chain),
            timestamp=str(datetime.datetime.now()),
            transactions=self.pending_transactions,
            proof=new_proof,
            previous_hash=previous_block.hash
        )

        # Resetear las transacciones pendientes y añadir el bloque a la cadena
        self.pending_transactions = []
        self.chain.append(new_block)

        return new_block

    def is_chain_valid(self) -> bool:
        """
        Verifica la validez de toda la cadena de bloques.
        
        Returns:
            bool: True si la cadena es válida, False en caso contrario
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verificar el hash actual
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verificar la conexión con el bloque anterior
            if current_block.previous_hash != previous_block.hash:
                return False

            # Verificar la prueba de trabajo
            hash_operation = hashlib.sha256(
                f'{current_block.proof**2 - previous_block.proof**2}'.encode()
            ).hexdigest()
            
            if hash_operation[:self.difficulty] != '0' * self.difficulty:
                return False

        return True

    def get_block_by_index(self, index: int) -> Optional[Block]:
        """
        Obtiene un bloque por su índice.
        
        Args:
            index: El índice del bloque a buscar
            
        Returns:
            Optional[Block]: El bloque si existe, None si no se encuentra
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def get_balance(self, address: str) -> float:
        """
        Calcula el balance de una dirección revisando todas las transacciones.
        
        Args:
            address: La dirección de la cual calcular el balance
            
        Returns:
            float: El balance actual de la dirección
        """
        balance = 0.0
        
        # Revisar todas las transacciones en todos los bloques
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['recipient'] == address:
                    balance += transaction['amount']
                if transaction['sender'] == address:
                    balance -= transaction['amount']
        
        return balance

    def get_transaction_history(self, address: str) -> List[Dict]:
        """
        Obtiene el historial de transacciones de una dirección.
        
        Args:
            address: La dirección de la cual obtener el historial
            
        Returns:
            List[Dict]: Lista de transacciones donde la dirección está involucrada
        """
        transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['sender'] == address or transaction['recipient'] == address:
                    transactions.append({
                        'block_index': block.index,
                        'timestamp': transaction['timestamp'],
                        'sender': transaction['sender'],
                        'recipient': transaction['recipient'],
                        'amount': transaction['amount']
                    })
                    
        return transactions

# Crear una instancia de Flask y la blockchain
app = Flask(__name__)
blockchain = Blockchain()

# Rutas de la API
@app.route('/mine', methods=['GET'])
def mine():
    """Endpoint para minar un nuevo bloque."""
    block = blockchain.mine_block("MinerAddress")  # En una implementación real, esto vendría del minero
    response = {
        'message': 'Nuevo bloque minado',
        'block': block.to_dict()
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Endpoint para crear una nueva transacción."""
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    
    if not all(k in values for k in required):
        return 'Faltan valores', 400

    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )
    
    response = {'message': f'La transacción se añadirá al bloque {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    """Endpoint para obtener la cadena completa."""
    response = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/chain/valid', methods=['GET'])
def validate_chain():
    """Endpoint para validar la cadena."""
    is_valid = blockchain.is_chain_valid()
    return jsonify({'valid': is_valid}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
