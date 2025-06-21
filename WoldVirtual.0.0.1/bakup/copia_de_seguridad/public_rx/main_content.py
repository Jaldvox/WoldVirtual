import reflex as rx
from .threejs_viewer import threejs_viewer
from .state import State

def main_content_area() -> rx.Component:
    """Zona principal de contenido, mostrando el visor 3D real como CustomComponent y el último evento recibido."""
    return rx.box(
        rx.box(
            rx.vstack(
                rx.text("Área de Contenido Principal", font_size="1.5em", font_weight="bold", color="#333"),
                threejs_viewer(
                    sceneData={"mensaje": "¡Hola desde Reflex!", "entidad": "Avatar", "pos": [0,1,2]},
                    on_event=State.handle_threejs_event
                ),
                rx.text("Aquí va el contenido principal de la aplicación.", font_size="1em", color="#666", text_align="center"),
                rx.text("El área se ajusta automáticamente al tamaño de la ventana.", font_size="0.9em", color="#888", text_align="center"),
                rx.box(
                    rx.text("Último evento recibido desde React:", font_size="0.9em", color="#444"),
                    rx.code(State.ultimo_evento if State.ultimo_evento else "(Sin eventos)",
                            font_size="0.85em", color="#0a0", background="#eee", padding="0.5em", border_radius="8px"),
                    margin_top="1em"
                ),
                spacing="2",
                align_items="center",
                justify_content="center",
                height="100%",
            ),
            background_color="white",
            border="2px solid #4A90E2",
            border_radius="30px",
            box_shadow="0 4px 20px rgba(0,0,0,0.1)",
            width="90%",
            height="85%",
            padding="2rem",
            margin="auto",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        width="100%",
        height="100%",
        background_color="#228B22",
        display="flex",
        align_items="center",
        justify_content="center",
        padding="2",
    ) 