"""
Aplicación principal de Wold Virtual 3D
Maneja las rutas y configuración de la aplicación Reflex
"""

from reflex import App
from components import *
from pages import *

# Configuración de la aplicación
app = App(
    name="Wold Virtual 3D",
    description="Aplicación 3D virtual con Reflex y Three.js",
    version="1.0.0"
)

# Definición de rutas principales
@app.route('/')
def home():
    """Página principal de la aplicación"""
    return HomePage()

@app.route('/about')
def about():
    """Página de información sobre la aplicación"""
    return AboutPage()

@app.route('/3d-scene')
def three_d_scene():
    """Página de escena 3D"""
    return ThreeDScenePage()

@app.route('/api/status')
def api_status():
    """Endpoint de estado de la API"""
    return {"status": "active", "version": "1.0.0"}

# Punto de entrada principal
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )