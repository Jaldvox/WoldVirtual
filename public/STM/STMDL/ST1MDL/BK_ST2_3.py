import hashlib
import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.crear_bloque_genesis()

    def crear_bloque_genesis(self):
        genesis_block = {
            'index': 0,
            'timestamp': str(datetime.datetime.now()),
            'data': 'Bloque Génesis',
            'previous_hash': '0',
            'hash': self.hash_block({
                'index': 0,
                'timestamp': str(datetime.datetime.now()),
                'data': 'Bloque Génesis',
                'previous_hash': '0'
            })
        }
        self.chain.append(genesis_block)

    def agregar_bloque(self, data):
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'timestamp': str(datetime.datetime.now()),
            'data': data,
            'previous_hash': previous_block['hash'],
            'hash': ''
        }
        new_block['hash'] = self.hash_block(new_block)
        self.chain.append(new_block)

    def obtener_informacion_cadena(self):
        informacion = {
            'longitud': len(self.chain),
            'bloques': self.chain
        }
        return informacion

    def hash_block(self, block):
        block_string = f"{block['index']}{block['timestamp']}{block['data']}{block['previous_hash']}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def validar_cadena(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            if current_block['hash'] != self.hash_block(current_block):
                return False
        return True
