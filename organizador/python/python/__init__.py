import hashlib
import time
import webbrowser
import os

def blockchain_manager(action='create', data=None, chain=None):
    """
    Unified blockchain management function that handles creation, addition, validation and printing of blocks
    Actions: 'create', 'add', 'validate', 'print'
    """
    def create_block(index, data, previous_hash):
        timestamp = time.time()
        return {
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'previous_hash': previous_hash,
            'hash': hashlib.sha256(f"{index}{timestamp}{data}{previous_hash}".encode()).hexdigest()
        }

    if action == 'create':
        return [create_block(0, "Bloque Génesis", "0")]
    
    if not chain:
        raise ValueError("Blockchain is required for this operation")
        
    if action == 'add':
        if not data:
            raise ValueError("Data is required to add a block")
        new_block = create_block(len(chain), data, chain[-1]['hash'])
        chain.append(new_block)
        return new_block
        
    if action == 'validate':
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i-1]
            if (current['hash'] != create_block(current['index'], current['data'], 
                current['previous_hash'])['hash'] or
                current['previous_hash'] != previous['hash']):
                return False
        return True
        
    if action == 'print':
        if not isinstance(data, dict) or 'index' not in data:
            raise ValueError("Valid block required for printing")
        print(f"\n==== Información del Bloque ===="
              f"\nÍndice: {data['index']}"
              f"\nTimestamp: {data['timestamp']}"
              f"\nDatos: {data['data']}"
              f"\nHash: {data['hash']}"
              f"\nHash Anterior: {data['previous_hash']}"
              f"\n============================")

# Example usage from main:
# 1. Create a new blockchain
# chain = blockchain_manager('create')
#
# 2. Add a new block
# new_block = blockchain_manager('add', data="Transaction data", chain=chain)
#
# 3. Validate the blockchain
# is_valid = blockchain_manager('validate', chain=chain)
#
# 4. Print a block
# blockchain_manager('print', data=new_block)
#
# Complete example:
# def main():
#     chain = blockchain_manager('create')
#     new_block = blockchain_manager('add', data="First transaction", chain=chain)
#     blockchain_manager('print', data=new_block)
#     is_valid = blockchain_manager('validate', chain=chain)
#     print(f"Blockchain is valid: {is_valid}")

def view_blockchain():
    """Opens blockchain visualization in browser"""
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_html = os.path.join(ruta_actual, 'html', 'web.html')
    webbrowser.open('file://' + ruta_html)

# Example usage:
# chain = manage_blockchain('create')
# new_block = manage_blockchain('add', data="Some data", chain=chain)
# is_valid = manage_blockchain('validate', chain=chain)
# manage_blockchain('print', data=new_block)
# view_blockchain()
