from flask import Flask, request, jsonify, render_template_string
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

# Página web de ejemplo
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Blockchain Demo</title>
</head>
<body>
    <h1>Bienvenido a la Blockchain</h1>
    <p>Esta es una demo de una blockchain simple en Python.</p>
    <form action="/add_block" method="post">
        <label for="data">Datos del bloque:</label><br>
        <input type="text" id="data" name="data"><br><br>
        <input type="submit" value="Agregar bloque">
    </form>
    <h2>Blockchain Actual</h2>
    <ul>
    {% for block in blockchain %}
        <li>
            <strong>Índice:</strong> {{ block['index'] }} <br>
            <strong>Hash:</strong> {{ block['hash'] }} <br>
            <strong>Datos:</strong> {{ block['data'] }} <br>
            <hr>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

# Endpoint para la página principal
@app.route('/')
def home():
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
    return render_template_string(HTML_TEMPLATE, blockchain=chain_data)

# Endpoint para agregar un nuevo bloque (formulario HTML)
@app.route('/add_block', methods=['POST'])
def add_block_html():
    global previous_block
    data = request.form.get('data')
    if not data:
        return "Faltan datos", 400

    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    previous_block = new_block
    return "<p>¡Bloque agregado exitosamente!</p><a href='/'>Regresar</a>"

if __name__ == '__main__':
    app.run(debug=True)
