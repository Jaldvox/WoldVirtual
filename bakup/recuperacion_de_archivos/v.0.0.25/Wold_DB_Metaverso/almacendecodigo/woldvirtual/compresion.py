import json
import gzip
import os # Importamos el módulo os para manejar directorios
import time # Importamos time para añadir un timestamp al estado

def comprimir_y_guardar_datos(datos, archivo_salida):
    try:
        datos_serializados = json.dumps(datos).encode('utf-8')
        datos_comprimidos = gzip.compress(datos_serializados)
        with open(archivo_salida, 'wb') as archivo:
            archivo.write(datos_comprimidos)
        print(f"Datos comprimidos y guardados en {archivo_salida}")
    except Exception as e:
        print(f"Error al comprimir y guardar datos: {e}")

def cargar_y_descomprimir_datos(archivo_entrada):
    try:
        with open(archivo_entrada, 'rb') as archivo:
            datos_comprimidos = archivo.read()
        datos_descomprimidos = gzip.decompress(datos_comprimidos)
        return json.loads(datos_descomprimidos)
    except Exception as e:
        print(f"Error al cargar y descomprimir datos: {e}")
        return None

def guardar_estado_plataforma(estado_data, directorio="status_logs", nombre_archivo="status.json"):
    """
    Guarda información de estado de la plataforma en un archivo JSON dentro de un directorio específico.
    Crea el directorio si no existe.
    """
    try:
        # Crear el directorio si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"Directorio '{directorio}' creado.")

        ruta_completa = os.path.join(directorio, nombre_archivo)

        # Añadir un timestamp a los datos de estado
        estado_data['timestamp'] = time.time()

        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(estado_data, f, indent=4)

        print(f"Información de estado guardada en {ruta_completa}")
    except Exception as e:
        print(f"Error al guardar información de estado: {e}")

# Ejemplo de cómo podrías usar la nueva función (esto no se ejecuta al importar)
# if __name__ == "__main__":
#     estado_ejemplo = {
#         "status": "operacional",
#         "message": "La plataforma está funcionando correctamente.",
#         "version": "1.0"
#     }
#     guardar_estado_plataforma(estado_ejemplo)
import json
import gzip

def comprimir_y_guardar_datos(datos, archivo_salida):
    try:
        datos_serializados = json.dumps(datos).encode('utf-8')
        datos_comprimidos = gzip.compress(datos_serializados)
        with open(archivo_salida, 'wb') as archivo:
            archivo.write(datos_comprimidos)
        print(f"Datos comprimidos y guardados en {archivo_salida}")
    except Exception as e:
        print(f"Error al comprimir y guardar datos: {e}")

def cargar_y_descomprimir_datos(archivo_entrada):
    try:
        with open(archivo_entrada, 'rb') as archivo:
            datos_comprimidos = archivo.read()
        datos_descomprimidos = gzip.decompress(datos_comprimidos)
        return json.loads(datos_descomprimidos)
    except Exception as e:
        print(f"Error al cargar y descomprimir datos: {e}")
        return None
