# Import necessary modules to potentially interact with them
from blockchain import Blockchain
# No necesitamos importar los otros módulos aquí directamente para la descripción,
# pero sí la clase Blockchain para obtener su hash.

# Define descripciones para cada módulo
module_descriptions = {
    "usuarios": "Gestiona el registro, autenticación y acciones de los usuarios, interactuando con la blockchain.",
    "recursos": "Administra la asignación y monitoreo de recursos (CPU, ancho de banda) para los usuarios.",
    "blockchain": "Implementa la cadena de bloques para almacenar transacciones de forma inmutable.",
    "database": "Proporciona funciones para conectar a una base de datos tradicional y cargar datos de la blockchain.",
    "compresion": "Maneja la compresión y descompresión de datos para almacenamiento eficiente.",
    "servidor": "Utiliza Flask y Socket.IO para servir la aplicación web y manejar la comunicación en tiempo real.",
    "main": "Punto de entrada principal que inicia el servidor web."
}

def get_module_info(blockchain_instance: Blockchain):
    """
    Recopila información (descripción y un hash relevante) para cada módulo.
    """
    info = {}
    for module_name, description in module_descriptions.items():
        module_info = {
            "description": description,
            "hash": "N/A" # Valor de hash por defecto
        }
        # Obtener hash específico para módulos donde sea relevante
        if module_name == "blockchain":
            # Obtener el hash del último bloque en la blockchain
            if blockchain_instance and blockchain_instance.chain:
                latest_block = blockchain_instance.chain[-1]
                # Asegurarse de que la instancia de blockchain tiene un método hash
                if hasattr(blockchain_instance, 'hash'):
                     module_info["hash"] = blockchain_instance.hash(latest_block)
                else:
                     module_info["hash"] = "Método hash no disponible en Blockchain"
            else:
                 module_info["hash"] = "Blockchain vacía o no inicializada"
        # Añadir lógica para otros módulos si se puede derivar un hash relevante de su estado
        # elif module_name == "usuarios":
        #     # Podríamos hashear la lista de usuarios registrados (si se almacena de forma hasheable)
        #     pass
        # elif module_name == "recursos":
        #     # Podríamos hashear el estado del monitoreo de recursos
        #     pass
        # ... añadir otros módulos según sea necesario

        info[module_name] = module_info
    return info

# Nota: app.py en sí mismo no ejecuta nada directamente en esta nueva estructura.
# Sus funciones/datos serán importados y utilizados por servidor.py.
from usuarios import registrar_usuario, verificar_credenciales, manejar_accion
from recursos import RecursosUsuario, asignar_recursos_a_usuario, MonitoreoRecursos
from blockchain import Blockchain
from database import conectar_base_datos
from compresion import comprimir_y_guardar_datos, cargar_y_descomprimir_datos
from servidor import app, socketio

def main():
    # Inicializar recursos
    recursos_usuario = RecursosUsuario(50, 50)  # Ejemplo de inicialización con 50% de CPU y ancho de banda

    # Conectar a la base de datos
    db = conectar_base_datos()

    # Crear un nuevo usuario
    registrar_usuario("nombre", "contraseña")

    # Ejecutar compresión de datos
    datos_usuario = {"nombre": "nombre", "datos": "datos_ejemplo"}
    comprimir_y_guardar_datos(datos_usuario, "datos_comprimidos.gz")

    # Procesar transacción en la blockchain
    blockchain = Blockchain()
    blockchain.agregar_bloque("transaccion_ejemplo")

    # Iniciar servidor
    socketio.run(app, debug=True)

if __name__ == "main":
    main()
