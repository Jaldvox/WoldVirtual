import hashlib
import json
from time import time
from typing import List, Dict, Any
from bk_ini import *
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

def blockchain_operation(operation_type: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            if operation_type == 'hash':
                block_string = json.dumps(args[0], sort_keys=True).encode()
                return hashlib.sha256(block_string).hexdigest()
            elif operation_type == 'transaction':
                return self._handle_transaction(*args)
            elif operation_type == 'mining':
                return self._handle_mining(*args)
            elif operation_type == 'validation':
                return self._validate_chain()
            elif operation_type == 'balance':
                return self._get_address_balance(*args)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_block = {
            'index': 0, 'timestamp': time(),
            'transactions': [], 'previous_hash': '0' * 64, 'nonce': 0
        }
        genesis_block['hash'] = self.process_operation('hash', genesis_block)
        self.chain.append(genesis_block)

    def _handle_transaction(self, sender: str, recipient: str, amount: float) -> None:
        self.pending_transactions.append({
            'sender': sender, 'recipient': recipient,
            'amount': amount, 'timestamp': time()
        })

    def _handle_mining(self, miner_address: str) -> Dict[str, Any]:
        if not self.pending_transactions:
            return None
        last_block = self.chain[-1]
        new_block = {
            'index': len(self.chain), 'timestamp': time(),
            'transactions': self.pending_transactions,
            'previous_hash': last_block['hash'], 'nonce': 0
        }
        self.pending_transactions = [{
            'sender': "network", 'recipient': miner_address,
            'amount': 10.0, 'timestamp': time()
        }]
        new_block['hash'] = self.process_operation('hash', new_block)
        self.chain.append(new_block)
        return new_block

    def _validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current, previous = self.chain[i], self.chain[i-1]
            if (current['hash'] != self.process_operation('hash', current) or
                current['previous_hash'] != previous['hash']):
                return False
        return True

    def _get_address_balance(self, address: str) -> float:
        balance = 0
        for block in self.chain:
            for tx in block['transactions']:
                if tx['sender'] == address:
                    balance -= tx['amount']
                if tx['recipient'] == address:
                    balance += tx['amount']
        return balance

    @blockchain_operation('hash')
    def process_operation(self, operation_type: str, *args, **kwargs) -> Any:
        pass
