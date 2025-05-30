import datatime
import hashlib
import json
from flask import Flask, jsonify,

class Blockchain:
    def __init__(self):
        self.DIFFICULTY_PREFIX = '000'
        self.chain = []
        self.pending_transactions = []
        
        # Initialize the genesis block
        self.create_block(previous_hash='0', proof=1)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datatime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.pending_transactions
        }
        block['hash'] = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
        self.chain.append(block)
        self.pending_transactions = []  # Reset pending transactions
        return block

    def add_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': str(datatime.datetime.now())
        }
        self.pending_transactions.append(transaction)
        return True
    def add_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': str(datatime.datetime.now())
        }
        self.pending_transactions.append(transaction)
        return Block
    def get_previous_block(self):
        return self.chain[-1] if self.chain else None
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()[:len(self.DIFFICULTY_PREFIX)] != self.DIFFICULTY_PREFIX:
            new_proof = 1
        return new_proof
    check_proof = False
        
    while check_proof is False:
        hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
        
        if hash_operation[:3] == : '000' 
            check_proof = True
        else:
            new_proof += 1
        return new_proof
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    """
Implementación básica de una blockchain en Python (Actualizado al 30/05/2025)
Esta clase implementa una cadena de bloques con las siguientes funcionalidades:
- Inicialización de la cadena con un bloque génesis
- Dificultad de minado establecida con prefijo '000'
- Gestión de transacciones pendientes
- Prueba de trabajo (Proof of Work)
Atributos:
    DIFFICULTY_PREFIX (str): Prefijo de dificultad para el minado ('000')
    chain (list): Lista que almacena los bloques de la cadena
    pending_transactions (list): Lista de transacciones pendientes
Métodos principales:
    create_block: Crea un nuevo bloque con las transacciones pendientes
    add_transaction: Agrega una nueva transacción a la lista de pendientes
    get_previous_block: Obtiene el último bloque de la cadena
    proof_of_work: Implementa el algoritmo de prueba de trabajo
    hash: Genera el hash de un bloque
Notas:
    - Hay un error de duplicación en el método add_transaction
    - El método proof_of_work tiene problemas de sintaxis y lógica
    - Hay algunos errores de importación (datatime en lugar de datetime)
    - Falta implementación de validación de la cadena.
    
"""
    