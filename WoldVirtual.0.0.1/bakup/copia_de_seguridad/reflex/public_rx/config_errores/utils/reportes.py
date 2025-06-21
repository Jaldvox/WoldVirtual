def generar_reporte(errores, correcciones):
    print("=== REPORTE DE ERRORES ===")
    for archivo, lista in errores.items():
        print(f"{archivo}:")
        for err in lista:
            print(f"  - {err}")
    print("\n=== CORRECCIONES APLICADAS ===")
    for archivo in correcciones:
        print(f"Corregido: {archivo}") 