import reflex as rx
import traceback

def mostrar_error_ui(mensaje: str) -> rx.Component:
    """Devuelve un componente de alerta para mostrar errores en la UI."""
    return rx.box(
        rx.text("Error:", color="red", font_weight="bold"),
        rx.text(mensaje, color="red"),
        background="#ffeaea",
        border="1px solid #ff0000",
        border_radius="8px",
        padding="1em",
        margin_y="1em"
    )

def loguear_excepcion(e: Exception):
    """Imprime la traza de error en consola y la devuelve como string."""
    traza = traceback.format_exc()
    print(f"Excepción capturada: {e}\n{traza}")
    return traza

def handler_seguro(func):
    """Decorador para capturar y mostrar errores en handlers Reflex."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            loguear_excepcion(e)
            # Aquí podrías actualizar el estado para mostrar el error en la UI
    return wrapper 