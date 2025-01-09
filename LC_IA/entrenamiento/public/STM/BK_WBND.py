from flask import Flask, request, render_template_string, redirect, url_for
import time
import hashlib

# Modelo de Bloque
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Modelo de Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []  # Inicializamos la cadena vacía
        self.create_genesis_block()  # Generamos explícitamente el bloque génesis

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)  # Añadimos el bloque génesis a la cadena

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, latest_block.hash)
        self.chain.append(new_block)

# Inicialización de Flask y Blockchain
app = Flask(__name__)
blockchain = Blockchain()  # Blockchain se inicializa y crea el bloque génesis

# Vistas HTML comunes
base_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}  WOLD VIRTUAL </h1>
    {{ body|safe }}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(
        base_template,
        title="Blockchain App",
        heading="Bienvenido a la App Blockchain",
        body='''<a href="/register">Registro</a> | <a href="/login">Iniciar Sesión</a>'''
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        blockchain.add_block(f"User Registered: {username}")
        return redirect(url_for('login'))
    return render_template_string(
        base_template,
        title="Registro",
        heading="Registro",
        body='''
        <form action="/register" method="post">
            <label for="username">Nombre de usuario:</label>
            <input type="text" id="username" name="username" required>
            <button type="submit">Registrarse</button>
        </form>
        '''
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        blockchain.add_block(f"User Logged In: {username}")
        return redirect(url_for('profile', username=username))
    return render_template_string(
        base_template,
        title="Iniciar Sesión",
        heading="Iniciar Sesión",
        body='''
        <form action="/login" method="post">
            <label for="username">Nombre de usuario:</label>
            <input type="text" id="username" name="username" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
        '''
    )

@app.route('/profile/<username>')
def profile(username):
    return render_template_string(
        base_template,
        title="Perfil",
        heading=f"Bienvenido, {username}",
        body='''<a href="/">Volver al inicio</a>'''
    )

@app.route('/chain')
def chain():
    chain_data = [
        {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }
        for block in blockchain.chain
    ]
    return {"chain": chain_data, "length": len(chain_data)}

if __name__ == '__main__':
    print("Blockchain inicializada. Bloque Génesis:")
    print(f"Índice: {blockchain.chain[0].index}, Data: {blockchain.chain[0].data}, Hash: {blockchain.chain[0].hash}")
    app.run(debug=True)
