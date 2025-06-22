import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def cargar_datos(ruta_archivo):
    """Cargar datos desde diferentes formatos"""
    if ruta_archivo.endswith('.csv'):
        return pd.read_csv(ruta_archivo)
    elif ruta_archivo.endswith('.json'):
        return pd.read_json(ruta_archivo)
    elif ruta_archivo.endswith('.xlsx'):
        return pd.read_excel(ruta_archivo)
    else:
        raise ValueError("Formato de archivo no soportado")

def limpiar_datos(datos):
    """Limpiar datos eliminando valores problemáticos"""
    # Eliminar valores nulos
    datos = datos.dropna()
    
    # Eliminar duplicados
    datos = datos.drop_duplicates()
    
    # Eliminar outliers usando IQR
    Q1 = datos.quantile(0.25)
    Q3 = datos.quantile(0.75)
    IQR = Q3 - Q1
    datos = datos[~((datos < (Q1 - 1.5 * IQR)) | (datos > (Q3 + 1.5 * IQR))).any(axis=1)]
    
    return datos

def preprocesar_datos(datos):
    """Preprocesar datos para entrenamiento"""
    # Separar variables numéricas y categóricas
    numericas = datos.select_dtypes(include=[np.number])
    categoricas = datos.select_dtypes(include=['object'])
    
    # Normalizar variables numéricas
    scaler = StandardScaler()
    numericas_norm = pd.DataFrame(
        scaler.fit_transform(numericas),
        columns=numericas.columns
    )
    
    # Codificar variables categóricas
    encoder = LabelEncoder()
    for col in categoricas.columns:
        categoricas[col] = encoder.fit_transform(categoricas[col])
    
    # Combinar datos procesados
    datos_procesados = pd.concat([numericas_norm, categoricas], axis=1)
    
    return datos_procesados, scaler, encoder