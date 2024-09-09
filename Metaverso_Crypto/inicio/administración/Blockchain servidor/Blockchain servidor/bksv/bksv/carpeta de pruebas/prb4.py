from flask import jsonify, request
from prb2 import registrar_actividad

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({'blockchain': blockchain})

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.get_json()
    if 'data' in data:
        new_block = {'index': len(blockchain) + 1, 'data': data['data']}
        blockchain.append(new_block)
        registrar_actividad(f"Bloque agregado: {new_block}")
        return jsonify({'message': 'Bloque agregado correctamente', 'block': new_block})
    else:
        return jsonify({'error': 'Datos no proporcionados'})

@app.route('/block/<int:block_index>', methods=['GET'])
def get_block(block_index):
    if 0 < block_index <= len(blockchain):
        return jsonify({'block': blockchain[block_index - 1]})
    else:
        return jsonify({'error': 'Índice de bloque inválido'})
        
