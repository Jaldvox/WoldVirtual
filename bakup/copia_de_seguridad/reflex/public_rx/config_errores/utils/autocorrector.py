import os
import re

def corregir_prints_sin_parentesis(path):
    with open(path, encoding="utf-8") as f:
        contenido = f.read()
    nuevo = re.sub(r'print ([^\(\n][^\n]*)', r'print(\1)', contenido)
    if nuevo != contenido:
        with open(path, "w", encoding="utf-8") as f:
            f.write(nuevo)
        return True
    return False

def autocorregir_directorio(raiz):
    cambios = []
    for carpeta, _, archivos in os.walk(raiz):
        for archivo in archivos:
            if archivo.endswith('.py'):
                path = os.path.join(carpeta, archivo)
                if corregir_prints_sin_parentesis(path):
                    cambios.append(path)
    return cambios 