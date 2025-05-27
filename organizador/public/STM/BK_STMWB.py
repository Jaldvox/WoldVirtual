import hashlib
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.size = len(str(self.__dict__).encode('utf-8'))

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') + 
                   str(self.data).encode('utf-8') + 
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(time.time(), "Bloque Génesis", "0")

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def get_size(self):
        return sum(block.size for block in self.chain)

blockchain = Blockchain()

# Datos de ejemplo para la página web (simulado)
secciones = {
    "Metaverso Crypto 3D": {
        "descripcion": "Metaverso Crypto 3D descentralizado",
        "contenido": "Próximamente en esta página principal, se darán más detalles sobre el proyecto. Tenemos diferentes secciones que explicarán su función, dentro de cada módulo programado en Python."
    },
    "Usuarios": {
        "descripcion": "Usuarios",
        "contenido": "El módulo de usuarios permite registrar nuevos usuarios, verificar credenciales y manejar acciones específicas para cada usuario."
    },
    "Seccion 3": {  # Ejemplo de otra sección
        "descripcion": "Sección 3",
        "contenido": "Contenido de la sección 3..."
    }
    # ... más secciones
}

# HTML, CSS y JavaScript incrustados como string
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Blockchain Demo</title>
    <style>
        body { font-family: sans-serif; }
        .seccion {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
            cursor: pointer;
        }
        #blockchain-info { margin-top: 20px; }
        #blockchain-info pre {
            background-color: #f0f0f0;
            padding: 10px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>Secciones</h1>

    {% for nombre, datos in secciones.items() %}
    <div class="seccion" onclick="addBlock('{{ nombre }}')">
        <h2>{{ nombre }}</h2>
        <p>{{ datos.descripcion }}</p>
        <p>{{ datos.contenido }}</p>
    </div>
    {% endfor %}

    <div id="blockchain-info">
        <h2>Blockchain Info</h2>
        <pre id="blockchain-data"></pre>
    </div>

    <script>
        const blockchainData = document.getElementById('blockchain-data');

        function updateBlockchainInfo() {
            fetch('/blockchain_data')
                .then(response => response.json())
                .then(data => {
                    blockchainData.textContent = JSON.stringify(data, null, 2);
                });
        }

        function addBlock(data) {
            fetch('/new_block', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data: data })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Bloque añadido:', data);
                updateBlockchainInfo();
            });
        }

        updateBlockchainInfo();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, secciones=secciones)

@app.route('/new_block', methods=['POST'])
def new_block():
    data = request.get_json()['data']
    blockchain.add_block(Block(time.time(), data, blockchain.chain[-1].hash))
    return jsonify({'message': 'Bloque añadido'})

@app.route('/blockchain_data')
def blockchain_data():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data)

if __name__ == '__main__':
    app.run(debug=True)