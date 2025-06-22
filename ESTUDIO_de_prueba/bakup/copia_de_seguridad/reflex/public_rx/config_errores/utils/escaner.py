import os
import re

def buscar_errores_en_archivo(path):
    errores = []
    try:
        with open(path, encoding="utf-8") as f:
            contenido = f.read()
        # Ejemplo: buscar prints sin paréntesis (Python 3)
        if re.search(r'print [^\(\n]', contenido):
            errores.append("Uso de print sin paréntesis (posible error de sintaxis Python 3)")
        # Ejemplo: buscar tabs mezclados con espacios
        if "\t" in contenido and "    " in contenido:
            errores.append("Mezcla de tabs y espacios en la indentación")
        # Puedes añadir más patrones aquí...
    except Exception as e:
        errores.append(f"Error al leer {path}: {e}")
    return errores

def escanear_directorio(raiz):
    reporte = {}
    for carpeta, _, archivos in os.walk(raiz):
        for archivo in archivos:
            if archivo.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                path = os.path.join(carpeta, archivo)
                errores = buscar_errores_en_archivo(path)
                if errores:
                    reporte[path] = errores
    return reporte 