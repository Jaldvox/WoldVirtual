import reflex as rx
from custom_components.three_d_viewer import ThreeDViewer

def main_content_area() -> rx.Component:
    return rx.box(
        rx.box(
            rx.vstack(
                rx.text("Área de Contenido Principal", font_size="1.5em", font_weight="bold", color="#333"),
                rx.text("Aquí va el contenido principal de la aplicación.", font_size="1em", color="#666", text_align="center"),
                rx.text("El área se ajusta automáticamente al tamaño de la ventana.", font_size="0.9em", color="#888", text_align="center"),
                # Integración real: visor 3D como custom component
                rx.box(
                    ThreeDViewer(),
                    width="100%",
                    margin_top="2em",
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