import preprocesamiento
import entrenamiento
import evaluacion
import prediccion

def main():
    ruta_archivo = "dataset.csv"
    
    datos = preprocesamiento.preprocesar_datos(ruta_archivo)
    modelo = entrenamiento.entrenar_modelo(datos)
    resultados = evaluacion.evaluar_modelo(modelo, datos)
    predicciones = prediccion.realizar_predicciones(modelo, datos)
    
    print("Resultados de la evaluación:", resultados)
    print("Predicciones:", predicciones)
    print("¡Proceso completado!")

if __name__ == "__main__":
    main()