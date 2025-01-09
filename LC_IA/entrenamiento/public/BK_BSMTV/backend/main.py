from flask import Flask
from backend.routes.user_routes import user_routes
from usuarios.usuarios import registrar_usuario, verificar_credenciales
from recursos.recursos import RecursosUsuario
from blockchain.Blockchain import Blockchain
from database.database import conectar_base_datos
from compresion.compresion import comprimir_y_guardar_datos, cargar_y_descomprimir_datos
from servidor.servidor import app as flask_app, socketio

# Crear la aplicación Flask
app = Flask(__name__)

# Registrar las rutas de la API
app.register_blueprint(user_routes)

# Inicialización de recursos y otros procesos
def inicializar_sistemas():
    # Inicializar recursos
    recursos_usuario = RecursosUsuario(50, 50)  # Ejemplo con 50% de CPU y ancho de banda
    print("Recursos de usuario inicializados.")

    # Conectar a la base de datos
    db = conectar_base_datos()
    print("Conexión a la base de datos establecida.")

    # Crear un nuevo usuario
    try:
        registrar_usuario("nombre", "contraseña")
        print("Usuario registrado con éxito.")
    except ValueError as e:
        print(e)

    # Verificar credenciales
    if verificar_credenciales("nombre", "contraseña"):
        print("Credenciales verificadas con éxito.")
    else:
        print("Credenciales incorrectas.")

    # Realizar compresión de datos
    datos_usuario = {"nombre": "nombre", "datos": "datos_ejemplo"}
    comprimir_y_guardar_datos(datos_usuario, "datos_comprimidos.gz")
    print("Datos comprimidos y guardados.")

    # Cargar y descomprimir datos
    datos_cargados = cargar_y_descomprimir_datos("datos_comprimidos.gz")
    print("Datos cargados y descomprimidos:", datos_cargados)

    # Procesar transacción en la blockchain
    blockchain = Blockchain()
    blockchain.agregar_bloque("transaccion_ejemplo")
    print("Transacción añadida a la blockchain.")

@app.route('/')
def home():
    return "Página de administración inicial"

@app.before_first_request
def before_first_request():
    print("Iniciando procesos...")
    inicializar_sistemas()

# Ejecutar servidor Flask con SocketIO
if __name__ == "__main__":
    print("Iniciando servidor web Flask...")
    socketio.run(flask_app, debug=True)


"""

from flask import Flask
from backend.routes.user_routes import user_routes

app = Flask(__name__)

# Configuración de rutas
app.register_blueprint(user_routes)

@app.route('/')
def home():
    return "Página de administración inicial"

if __name__ == '__main__':
    app.run(debug=True)
