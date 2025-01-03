from flask import Flask, request, jsonify
import hashlib
import time

# Clase para representar un bloque
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

# Función para calcular el hash de un bloque
def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

# Crear el bloque génesis
def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

# Crear un nuevo bloque basado en el bloque anterior
def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Inicializar la blockchain con el bloque génesis
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Crear la aplicación Flask
app = Flask(__name__)

# Endpoint para obtener toda la blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = [
        {
            "index": block.index,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash
        }
        for block in blockchain
    ]
    return jsonify(chain_data)

# Endpoint para agregar un nuevo bloque
@app.route('/add_block', methods=['POST'])
def add_block():
    global previous_block
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    previous_block = new_block
    return jsonify({
        "message": "Bloque agregado exitosamente",
        "block": {
            "index": new_block.index,
            "previous_hash": new_block.previous_hash,
            "timestamp": new_block.timestamp,
            "data": new_block.data,
            "hash": new_block.hash
        }
    }), 201

# Endpoint para ver el bloque génesis
@app.route('/genesis', methods=['GET'])
def get_genesis_block():
    genesis_block = blockchain[0]
    return jsonify({
        "index": genesis_block.index,
        "previous_hash": genesis_block.previous_hash,
        "timestamp": genesis_block.timestamp,
        "data": genesis_block.data,
        "hash": genesis_block.hash
    })

if __name__ == '__main__':
    app.run(debug=True)
           
