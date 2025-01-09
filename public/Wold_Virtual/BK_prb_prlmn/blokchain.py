# <<<<<<< WoldVirtual.0.0.1
# Refactorizar en módulos más pequeños  
# copia de recuperación.
=======
# <<<<<<< BK_CPSG
# Refactorizar en módulos #
# >>>>>>> WoldVirtual.0.0.1

"""
# bloque central de la plataforma Notas #

#__version__ = "0.0.1"

#class MyCode:
    #def __init__(self):
        #pass

    #def run(self):
        print(f"Ejecutando la versión: {__version__}")

#if __name__ == "__main__":
    #my_code_instance = MyCode()
    #my_code_instance.run()

# import tkinter as tk
# =======
# >>>>>>> WoldVirtual.0.0.1
import hashlib
import time
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)

# Blockchain y clases relacionadas
class Bloque:
    def __init__(self, index, timestamp, datos, hash_anterior):
        self.index = index
        self.timestamp = timestamp
        self.datos = datos
        self.hash_anterior = hash_anterior
        self.nonce = 0
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        datos_codificados = f"{self.index}{self.timestamp}{self.datos}{self.hash_anterior}{self.nonce}"
        return hashlib.sha256(datos_codificados.encode('utf-8')).hexdigest()

    def proof_of_work(self, dificultad):
        while self.hash[:dificultad] != '0' * dificultad:
            self.nonce += 1
            self.hash = self.calcular_hash()

class CadenaBloques:
    def __init__(self):
        self.cadena = []
        self.crear_bloque_genesis()

    def crear_bloque_genesis(self):
        genesis_block = Bloque(0, time.time(), "Bloque Génesis", "0")
        self.cadena.append(genesis_block)

    def agregar_bloque(self, datos):
        hash_anterior = self.cadena[-1].hash
        nuevo_bloque = Bloque(len(self.cadena), time.time(), datos, hash_anterior)
        nuevo_bloque.proof_of_work(4)
        self.cadena.append(nuevo_bloque)

    def validar_cadena(self):
        for i in range(1, len(self.cadena)):
            bloque_actual = self.cadena[i]
            bloque_anterior = self.cadena[i - 1]
            if bloque_actual.hash != bloque_actual.calcular_hash() or bloque_actual.hash_anterior != bloque_anterior.hash:
                return False
        return True

# Inicializar la blockchain
mi_blockchain = CadenaBloques()

# Rutas de la aplicación Flask
@app.route('/informacion_cadena', methods=['GET'])
def informacion_cadena():
    informacion = {
        'longitud': len(mi_blockchain.cadena),
        'bloques': [block.__dict__ for block in mi_blockchain.cadena]
    }
    return jsonify(informacion), 200

@app.route('/nuevo_bloque', methods=['POST'])
def nuevo_bloque():
    datos = request.get_json().get('datos')
    mi_blockchain.agregar_bloque(datos)
    return jsonify({'mensaje': 'Nuevo bloque agregado'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
