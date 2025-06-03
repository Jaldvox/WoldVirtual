def preprocesar_datos(ruta_archivo):
    import pandas as pd

    # Cargar los datos desde el archivo
    datos = pd.read_csv(ruta_archivo)

    # Realizar el preprocesamiento necesario
    # Ejemplo: eliminar filas con valores nulos
    datos = datos.dropna()

    # Normalizar o escalar los datos si es necesario
    # Aquí puedes agregar más pasos de preprocesamiento según tus necesidades

    return datos