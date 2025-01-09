# IA1pn.py - Módulo principal que importa los demás módulos

import IA2pn
import IA3pn
import IA4pn
import IA5pn
import IA6pn
import IA1pn1


def preparar_datos(ruta_archivo):
    print("Preparando los datos...")
    return IA2pn.preprocesar_datos(ruta_archivo)


def entrenar_modelo(datos):
    print("Entrenando el modelo...")
    return IA3pn.entrenar_modelo(datos)


def evaluar_modelo(modelo, datos):
    print("Evaluando el modelo...")
    return IA4pn.evaluar_modelo(modelo, datos)


def realizar_predicciones(modelo, datos):
    print("Realizando predicciones...")
    return IA5pn.realizar_predicciones(modelo, datos)


def guardar_resultados(predicciones):
    print("Guardando resultados...")
    IA6pn.guardar_resultados(predicciones)


def main():
    IA1pn1.main()  # Llamamos al método `main` del archivo IA1pn1.py
    
    datos = preparar_datos("dataset.csv")
    modelo = entrenar_modelo(datos)
    resultados = evaluar_modelo(modelo, datos)
    predicciones = realizar_predicciones(modelo, datos)
    guardar_resultados(predicciones)
    
    print("¡Proceso completado!")


if __name__ == "__main__":
    main()
