from utils import escaner, autocorrector, reportes
import os

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.abspath(__file__))
    print(f"Escaneando errores en: {raiz}\n")
    errores = escaner.escanear_directorio(raiz)
    print("Errores encontrados:")
    for archivo, lista in errores.items():
        print(f"{archivo}:")
        for err in lista:
            print(f"  - {err}")
    print("\nAplicando autocorrecciones...\n")
    correcciones = autocorrector.autocorregir_directorio(raiz)
    reportes.generar_reporte(errores, correcciones) 