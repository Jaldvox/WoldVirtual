# IA2pn.py - Preprocesamiento de los datos

import pandas as pd

def preprocesar_datos(archivo_csv):
    # Cargar el dataset
        data = pd.read_csv(archivo_csv)
            
                # Ejemplo simple: Eliminar columnas nulas y normalizar los datos
                    data = data.dropna()
                        data_normalizada = (data - data.mean()) / data.std()
                            
                                return data_normalizada