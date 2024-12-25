from flask import Flask, jsonify, request
import json
import requests
from BK_ST2_1 import cargar_blockchain, agregar_bloque, guardar_blockchain
from BK_ST2_1_sincronizacion import sincronizar_blockchain

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
    guardar_blockchain(blockchain)
    return "Bloque agregado", 200

# Función para iniciar el servidor del nodo
def iniciar_servidor():
    app.run(port=5000)

if __name__ == "__main__":
    iniciar_servidor()
