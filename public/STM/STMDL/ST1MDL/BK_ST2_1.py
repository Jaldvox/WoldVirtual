from flask import Flask, request, jsonify, render_template
from ST1MDL.blockchain import Blockchain

# Inicializar Flask y la blockchain
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    """
    Página principal: carga el HTML desde una plantilla.
    """
    return render_template('index.html')

@app.route('/nuevo_bloque', methods=['GET'])
def nuevo_bloque():
    """
    Genera un nuevo bloque en la blockchain basado en los datos recibidos por parámetros.
    """
    prueba = request.args.get('prueba')
    hash_anterior = request.args.get('hash_anterior')

    # Validar los parámetros requeridos
    if not prueba or not hash_anterior:
        return jsonify({"error": "Parámetros 'prueba' y 'hash_anterior' son requeridos"}), 400

    # Crear y añadir un nuevo bloque
    nuevo_bloque = blockchain.add_block(prueba, hash_anterior)

    response = {
        "mensaje": "Nuevo bloque generado con éxito",
        "bloque": nuevo_bloque
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
