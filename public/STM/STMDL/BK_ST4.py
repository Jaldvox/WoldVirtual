# modulos/BK_ST4.py

def manejar_accion(usuario, accion):
    """
    Realiza una acción específica para el usuario.
    """
    if accion == "explorar":
        print(f"Bienvenido/a {usuario} al entorno de exploración.")
    elif accion == "intercambiar":
        print(f"Realizando intercambio para {usuario}.")
    else:
        print(f"Error: Acción '{accion}' no reconocida.")
