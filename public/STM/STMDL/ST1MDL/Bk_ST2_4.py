# BK_ST2_4.py - Funciones para la configuración y arranque del servidor del nodo
""""
from flask import Flask, jsonify, request
from BK_ST2_1 import cargar_blockchain, agregar_bloque
from BK_ST2_3 import sincronizar_blockchain

app = Flask(__name__)

# Cargar la blockchain localmente
blockchain = cargar_blockchain()

@app.route('/blockchain', methods=['GET'])
def obtener_blockchain():
    return jsonify(blockchain), 200

@app.route('/nuevo_bloque', methods=['POST'])
def agregar_bloque_r():
    datos = request.get_json()
    nuevo_bloque = datos['bloque']
    blockchain.append(nuevo_bloque)  # Valida el bloque antes de agregarlo
    agregar_bloque(blockchain, nuevo_bloque['data'])
    return "Bloque agregado", 200

# Función para iniciar el servidor del nodo
def iniciar_servidor():
    app.run(port=5000)
