# Este archivo ahora contendrá el backend web para compartir recursos informáticos.

from flask import Flask, request, jsonify

# Crear una instancia de la aplicación Flask

app = Flask(__name__)

# --- Rutas de ejemplo para el backend ---

@app.route('/')
def index():
    """Ruta de inicio simple para verificar que el servidor está funcionando."""
    return "Backend de Compartición de Recursos Informáticos funcionando."

@app.route('/status', methods=['GET'])
def status():
    """Ruta para obtener el estado del backend."""
    return jsonify({"status": "ok", "message": "Servidor listo para recibir solicitudes."})

# --- Aquí se añadirán más rutas para: ---
# - Registro de PCs que ofrecen recursos
# - Reporte de recursos disponibles (ancho de banda, etc.)
# - Solicitudes de recursos del metaverso
# - Orquestación de conexiones
# - etc.

# --- Lógica de ejecución del servidor ---
if __name__ == '__main__':
    # En un entorno de producción, usarías un servidor WSGI como Gunicorn o uWSGI.
    # Para desarrollo, podemos usar el servidor integrado de Flask.
    # debug=True permite recarga automática y mensajes de error detallados.
    print("Iniciando servidor Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000) # Escuchar en todas las interfaces en el puerto 5000
