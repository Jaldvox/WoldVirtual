import datetime
import hashlib
import json

class Blockchain:

    def blockchain_mine(chain=None,               difficulty_prefix='000'):
    # Inicializa la cadena si no existe
    if chain is None or len(chain) == 0:
        genesis = {
            'index': 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'proof': 1,
            'previous_hash': '0'
        }
        chain = [genesis]
        return chain
    # Minado
    previous_block = chain[-1]
    previous_proof = previous_block['proof']
    new_proof = 1
    while True:
        guess = f"{new_proof**2 - previous_proof**2}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        if guess_hash.startswith(difficulty_prefix):
            break
        new_proof += 1
    previous_hash = hashlib.sha256(json.dumps(previous_block, sort_keys=True).encode()).hexdigest()
    block = {
        'index': len(chain) + 1,
        'timestamp': datetime.datetime.now().isoformat(),
        'proof': new_proof,
        'previous_hash': previous_hash
    }
    chain.append(block)
    return chain