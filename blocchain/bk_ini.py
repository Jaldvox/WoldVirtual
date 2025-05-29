import datetime
import hashlib
# Removed unused imports Flask and jsonify

class Blockchain:
    DIFFICULTY_PREFIX = '0000'

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

    def mine_new_block(self, previous_proof):
        # Combines mine_block, proof_of_work and hash functions into one
        new_proof = 1
        check_proof = lambda p: hashlib.sha256(str(p**2 - previous_proof**2).encode()).hexdigest()[:len(self.DIFFICULTY_PREFIX)] == self.DIFFICULTY_PREFIX
        
        while not check_proof(new_proof):
            new_proof += 1
        import json
        new_hash = hashlib.sha256(json.dumps(previous_block, sort_keys=True).encode()).hexdigest()
        previous_block = self.chain[-1]
        new_hash = hashlib.sha256(str(previous_block).encode()).hexdigest()
        
        return self.create_block(proof=new_proof, previous_hash=new_hash)
