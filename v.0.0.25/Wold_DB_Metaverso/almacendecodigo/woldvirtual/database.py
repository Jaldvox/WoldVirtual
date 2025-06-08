import psycopg2
from psycopg2 import sql
# Importamos la clase Blockchain para poder leer sus datos
from blockchain import Blockchain

def conectar_base_datos():
    
    """
    Función para conectar a una base de datos PostgreSQL.
    Se mantiene para posible uso futuro con datos no relacionados con usuarios.
    
    """
    
    conexion = None
    try:
        # NOTA: Reemplaza estos datos con los de tu base de datos PostgreSQL real
        conexion = psycopg2.connect(
            database="tu_base_datos",
            user="tu_usuario",
            password="tu_contraseña",
            host="tu_host",
            port="tu_puerto"
        )
        print("Conexión a la base de datos PostgreSQL establecida.")
        # Ejemplo de consulta (puedes eliminar o modificar esto)
        # with conexion.cursor() as cursor:
        #     cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('usuarios')))
        #     resultados = cursor.fetchall()
        #     print("Resultados de ejemplo de la base de datos:")
        #     for resultado in resultados:
        #         print(resultado)
        return conexion # Retornamos la conexión si es exitosa
        
    except Exception as e:
        print(f"Error en la conexión a la base de datos PostgreSQL: {e}")
        return None # Retornamos None si falla la conexión
    # finally:
    #     # No cerramos la conexión aquí, debería cerrarse explícitamente cuando ya no se necesite
    #     if conexion:
    #         conexion.close()
    #         print("Conexión cerrada.")

def cargar_datos_desde_blockchain(blockchain: Blockchain):
    """
    Carga y retorna todos los datos (transacciones) almacenados en la blockchain.
    """
    datos_blockchain = []
    # Recorremos los bloques minados
    for block in blockchain.chain:
        # Asumimos que los datos del bloque son una lista de transacciones
        if isinstance(block.get('data'), list):
            datos_blockchain.extend(block['data'])
        elif block.get('data') is not None:
             # Si el dato no es una lista (como el bloque génesis), lo añadimos directamente
             datos_blockchain.append(block['data'])

    # Añadimos las transacciones pendientes
    datos_blockchain.extend(blockchain.pending_transactions)

    print(f"Cargados {len(datos_blockchain)} elementos de datos desde la blockchain.")
    return datos_blockchain

# Puedes añadir otras funciones aquí para interactuar con la base de datos tradicional
# o para procesar los datos cargados de la blockchain.

# import psycopg2
# from psycopg2 import sql

def conectar_base_datos():
    conexion = None
    try:
        conexion = psycopg2.connect(
            database="tu_base_datos",
            user="tu_usuario",
            password="tu_contraseña",
            host="tu_host",
            port="tu_puerto"
        )
        with conexion.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('usuarios')))
            resultados = cursor.fetchall()
            for resultado in resultados:
                print(resultado)
    except Exception as e:
        print(f"Error en la conexión a la base de datos: {e}")
    finally:
        if conexion:
            conexion.close()
    print("Conexión cerrada.")
