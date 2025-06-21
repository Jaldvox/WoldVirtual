import hashlib
import json
from time import time
from typing import List, Dict, Any
from bk_ini  import *
from functools import wraps
from typing import Callable, Any

"""
Módulo de implementación simple de blockchain que maneja operaciones básicas de criptomonedas.
Este módulo proporciona una clase Blockchain que implementa operaciones fundamentales
incluyendo manejo de transacciones, minería, validación de cadena y seguimiento de saldos.

Clases:
    Blockchain: Clase principal que implementa la funcionalidad de blockchain.

Funciones:
    blockchain_operation: Decorador que maneja diferentes operaciones de blockchain según el tipo.
        Args:
            operation_type (str): Tipo de operación ('hash', 'transaction', 'mining', 'validation', 'balance')
        Returns:
            Callable: Función decorada que procesa la operación especificada

Métodos de Clase:
    __init__(): Inicializa una nueva blockchain con una cadena vacía y transacciones pendientes.
    _create_genesis_block(): Crea y añade el primer bloque (génesis) a la cadena.
    _handle_transaction(sender: str, recipient: str, amount: float): Añade una nueva transacción a la lista pendiente.
    _handle_mining(miner_address: str): Crea un nuevo bloque con transacciones pendientes y lo añade a la cadena.
    _validate_chain(): Verifica la integridad de toda la blockchain.
    _get_address_balance(address: str): Calcula el saldo para una dirección dada.
    process_operation(operation_type: str, *args, **kwargs): Procesa diferentes operaciones de blockchain.

Atributos:
    chain (List): La blockchain principal que contiene todos los bloques confirmados
    pending_transactions (List): Almacenamiento temporal para transacciones no confirmadas

Nota:
    Esta implementación incluye prueba de trabajo básica y manejo simple de transacciones.
    Está destinada para fines educativos y no debe usarse en entornos de producción.
    
"""

class BlockchainSimple:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self._initialize_blockchain()

    def _initialize_blockchain(self):
        # Create genesis block automatically on initialization
        self.chain.append(self.blockchain_manager('create_block', 0, [], '0' * 64))

    def blockchain_manager(self, operation: str, *args) -> Any:
        """
        Single function to handle all blockchain operations.
        
        Args:
            operation: Type of operation ('create_block', 'transaction', 'mining', 'validate', 'balance', 'hash')
            *args: Additional arguments depending on operation
        """
        if operation == 'create_block':
            # Create a new block
            block = {
                'index': args[0],
                'timestamp': time(),
                'transactions': args[1],
                'previous_hash': args[2],
                'nonce': 0
            }
            block['hash'] = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
            return block

        elif operation == 'transaction':
            # Add new transaction
            self.pending_transactions.append({
                'sender': args[0],
                'recipient': args[1],
                'amount': args[2],
                'timestamp': time()
            })
            return True

        elif operation == 'mining':
            # Mine new block
            if not self.pending_transactions:
                return None
            
            reward_tx = {
                'sender': "network",
                'recipient': args[0],
                'amount': 10.0,
                'timestamp': time()
            }
            
            new_block = self.blockchain_manager('create_block',
                len(self.chain),
                self.pending_transactions + [reward_tx],
                self.chain[-1]['hash']
            )
            self.chain.append(new_block)
            self.pending_transactions = []
            return new_block

        elif operation == 'balance':
            # Calculate balance for address
            balance = 0
            for block in self.chain:
                for tx in block['transactions']:
                    if tx['recipient'] == args[0]:
                        balance += tx['amount']
                    if tx['sender'] == args[0]:
                        balance -= tx['amount']
            return balance

        elif operation == 'validate':
            # Validate entire chain
            for i in range(1, len(self.chain)):
                current = self.chain[i]
                previous = self.chain[i-1]
                
                # Verify hash
                current_hash = hashlib.sha256(json.dumps({**current, 'hash': None}, 
                    sort_keys=True).encode()).hexdigest()
                if current['hash'] != current_hash:
                    return False
                    
                # Verify chain link
                if current['previous_hash'] != previous['hash']:
                    return False
            return True

        elif operation == 'hash':
            # Generate hash for data
            return hashlib.sha256(json.dumps(args[0], sort_keys=True).encode()).hexdigest()

        return None
"""
Este módulo proporciona una clase BlockchainSimple que implementa operaciones fundamentales
Este módulo complementa al anterior (bk_ini) proporcionando una implementación más eficiente porque:
1. Unifica todas las operaciones en un solo gestor (blockchain_manager) reduciendo la duplicación de código
2. Simplifica el mantenimiento al centralizar la lógica en un único punto de control
3. Mejora la consistencia al manejar todas las operaciones de manera uniforme
4. Facilita la extensibilidad al permitir agregar nuevas operaciones fácilmente
5. Reduce la complejidad del código al eliminar múltiples métodos dispersos
Métodos Principales:
    _initialize_blockchain(): Inicializa la blockchain creando el bloque génesis.
    blockchain_manager(operation: str, *args): Gestiona todas las operaciones de blockchain.
Operaciones Soportadas en blockchain_manager:
    - 'create_block': Crea un nuevo bloque
    - 'transaction': Añade una nueva transacción
    - 'mining': Realiza el proceso de minería
    - 'balance': Calcula el saldo de una dirección
    - 'validate': Valida la integridad de la cadena
    - 'hash': Genera hash para los datos
    Esta implementación mejora la anterior al proporcionar una estructura más modular y mantenible,
    ideal para desarrollos educativos y prototipos. No se recomienda para uso en producción.


""""




