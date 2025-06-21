# IA6pn.py - Guardar los resultados

import pandas as pd

def guardar_resultados(predicciones):
    # Guardar las predicciones en un archivo CSV
        df_predicciones = pd.DataFrame(predicciones, columns=["Predicción"])
            df_predicciones.to_csv("resultados.csv", index=False)
                print("Resultados guardados en 'resultados.csv'.")
        