import datetime
import hashlib
from flask import Flask, jsonify,

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def mine_block(self, previous_proof):
        new_proof = 1
        while hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()[:4] != '0000':
            new_proof += 1
        
        previous_block = self.chain[-1]
        block = self.create_block(
            proof=new_proof,
            previous_hash=hashlib.sha256(str(previous_block).encode()).hexdigest()
        )
        return block
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()[:4] != '0000':
            new_proof += 1
        return new_proof
    def hash(self, block):
        encoded_block = str(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()