# Importamos solo lo necesario para ejecutar el servidor
"""
Módulo principal de ejecución para la plataforma WoldVirtual.

Este script sirve como punto de entrada para el sistema WoldVirtual, coordinando varios módulos
y funcionalidades:

Módulos coordinados:
- usuarios: Maneja registro, autenticación y acciones de usuarios
- recursos: Gestiona y monitorea recursos del sistema (CPU, ancho de banda)
- blockchain: Implementa funcionalidad blockchain para transacciones seguras
- database: Maneja conexiones y operaciones de base de datos
- compresion: Gestiona compresión y descompresión de datos
- servidor: Implementación del servidor web con soporte Socket.IO

Funcionalidades principales:
1. Gestión de Recursos del Sistema:
    - Inicializa recursos de usuario con límites específicos de CPU y ancho de banda
    - Monitorea uso de recursos

2. Gestión de Usuarios:
    - Maneja registro de usuarios
    - Valida credenciales
    - Procesa acciones de usuarios

3. Gestión de Datos:
    - Comprime y almacena datos de usuario
    - Carga y descomprime datos almacenados
    - Gestiona persistencia de datos

4. Operaciones Blockchain:
    - Inicializa blockchain
    - Procesa y añade transacciones a bloques

5. Servidor Web:
    - Inicia servidor Flask con soporte Socket.IO
    - Maneja peticiones web y comunicaciones en tiempo real

El script utiliza bloques try-except para manejo de errores e incluye registro básico
mediante declaraciones print para propósitos de desarrollo.

Uso:
    Ejecutar este script directamente para iniciar la plataforma WoldVirtual:
    python main.py
    
"""
from servidor import app, socketio

def main():
    # Las inicializaciones de Blockchain y otros módulos
    # ahora se manejan dentro de servidor.py o sus propios archivos.
    # Eliminamos las llamadas directas de ejemplo.

    # Iniciar servidor
    print("Iniciando servidor web...")
    # La instancia de blockchain se gestiona en servidor.py
    socketio.run(app, debug=True)

# Aseguramos que el script se ejecute solo cuando es el punto de entrada principal
if __name__ == "__main__":
    main()
from usuarios import registrar_usuario, verificar_credenciales, manejar_accion
from recursos import RecursosUsuario, MonitoreoRecursos
from blockchain import Blockchain
from database import conectar_base_datos
from compresion import comprimir_y_guardar_datos, cargar_y_descomprimir_datos
from servidor import app, socketio

def main():
    # Inicializar recursos
    recursos_usuario = RecursosUsuario(50, 50)  # Ejemplo de inicialización con 50% de CPU y ancho de banda
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

    # Verificar credenciales del usuario
    if verificar_credenciales("nombre", "contraseña"):
        print("Credenciales verificadas con éxito.")
    else:
        print("Credenciales incorrectas.")

    # Ejecutar compresión de datos
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

    # Iniciar servidor
    print("Iniciando servidor web...")
    socketio.run(app, debug=True)

if __name__ == "__main__":
    main()
