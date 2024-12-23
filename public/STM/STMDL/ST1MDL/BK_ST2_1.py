from flask import Flask, request, jsonify

app = Flask(__name__)

# HTML code as a multi-line string
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blockchain Demo</title>
</head>
<body>
    <h1>Blockchain Demo</h1>
    
    <button onclick="generarNuevoBloque()">Generar Nuevo Bloque</button>
    <div id="resultado"></div>

    <script>
        function generarNuevoBloque() {
            fetch('/nuevo_bloque?prueba=123&hash_anterior=abc')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('resultado').innerHTML = `<p>${data.mensaje}</p><pre>${JSON.stringify(data.bloque, null, 2)}</pre>`;
                })
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return html_code

@app.route('/nuevo_bloque', methods=['GET'])
def nuevo_bloque():
    prueba = request.args.get('prueba')
    hash_anterior = request.args.get('hash_anterior')
    
    # Aquí debes generar el nuevo bloque usando `prueba` y `hash_anterior`
    nuevo_bloque = {
        "index": 1,
        "timestamp": "2024-12-23T15:53:11",
        "datos": prueba,
        "hash_anterior": hash_anterior,
        "hash": "nuevo_hash_generado"
    }
    
    response = {
        "mensaje": "Nuevo bloque generado con éxito",
        "bloque": nuevo_bloque
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
