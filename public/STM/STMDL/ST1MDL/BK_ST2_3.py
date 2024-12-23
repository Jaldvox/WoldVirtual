import json
import gzip

def comprimir_datos(datos):
    """
    Serializa y comprime los datos proporcionados.
    
    :param datos: Los datos a serializar y comprimir (deben ser serializables en JSON).
    :return: Bytes comprimidos.
    :raises: Exception si hay un error durante el proceso.
    """
    try:
        datos_serializados = json.dumps(datos).encode('utf-8')
        return gzip.compress(datos_serializados)
    except Exception as e:
        raise ValueError(f"Error al comprimir los datos: {e}")

def guardar_datos_comprimidos(datos_comprimidos, archivo_salida):
    """
    Guarda datos comprimidos en un archivo.
    
    :param datos_comprimidos: Bytes comprimidos a guardar.
    :param archivo_salida: Ruta del archivo de salida.
    :raises: Exception si hay un error durante el proceso.
    """
    try:
        with open(archivo_salida, 'wb') as archivo:
            archivo.write(datos_comprimidos)
        print(f"Datos guardados en {archivo_salida}")
    except Exception as e:
        raise IOError(f"Error al guardar datos en {archivo_salida}: {e}")

def comprimir_y_guardar_datos(datos, archivo_salida):
    """
    Serializa, comprime y guarda los datos en un archivo.
    
    :param datos: Los datos a serializar y comprimir.
    :param archivo_salida: Ruta del archivo donde se guardarán los datos comprimidos.
    """
    try:
        datos_comprimidos = comprimir_datos(datos)
        guardar_datos_comprimidos(datos_comprimidos, archivo_salida)
    except Exception as e:
        print(f"Error en el proceso de compresión y guardado: {e}")

def cargar_datos_comprimidos(archivo_entrada):
    """
    Carga datos comprimidos desde un archivo.
    
    :param archivo_entrada: Ruta del archivo de entrada.
    :return: Bytes comprimidos leídos del archivo.
    :raises: Exception si hay un error durante el proceso.
    """
    try:
        with open(archivo_entrada, 'rb') as archivo:
            return archivo.read()
    except Exception as e:
        raise IOError(f"Error al cargar datos desde {archivo_entrada}: {e}")

def descomprimir_datos(datos_comprimidos):
    """
    Descomprime y deserializa datos comprimidos.
    
    :param datos_comprimidos: Bytes comprimidos a descomprimir.
    :return: Datos deserializados (objeto Python).
    :raises: Exception si hay un error durante el proceso.
    """
    try:
        datos_descomprimidos = gzip.decompress(datos_comprimidos)
        return json.loads(datos_descomprimidos)
    except Exception as e:
        raise ValueError(f"Error al descomprimir los datos: {e}")

def cargar_y_descomprimir_datos(archivo_entrada):
    """
    Carga y descomprime datos desde un archivo.
    
    :param archivo_entrada: Ruta del archivo comprimido.
    :return: Datos deserializados (objeto Python) o None en caso de error.
    """
    try:
        datos_comprimidos = cargar_datos_comprimidos(archivo_entrada)
        return descomprimir_datos(datos_comprimidos)
    except Exception as e:
        print(f"Error en el proceso de carga y descompresión: {e}")
        return None
