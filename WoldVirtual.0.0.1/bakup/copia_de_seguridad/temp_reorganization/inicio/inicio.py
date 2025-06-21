"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

def header() -> rx.Component:
    return rx.hstack(
        rx.text("World Virtual", font_size="1.2em", color="black", font_weight="bold"),
        rx.spacer(),
        rx.text("Mapa del proyecto.", margin_left="0.5em", color="black", font_size="0.8em"),
        rx.text("Libro blanco", margin_left="0.5em", color="black", font_size="0.8em"),
        rx.text("Código abierto", margin_left="0.5em", color="black", font_size="0.8em"),
        rx.button(
            "Redes Blockchain",
            bg="#343a40",
            color="white",
            margin_left="0.5em",
            font_size="0.65em",
            padding="0.3em 0.6em",
            border_radius="4px",
        ),
        width="100%",
        height="50px",
        background_color="#FFD700",
        align_items="center",
        padding_x="4",
        z_index="100",
        position="relative",
    )

def main_content_area() -> rx.Component:
    return rx.box(
        rx.box(
            rx.vstack(
                rx.text("Área de Contenido Principal", 
                        font_size="1.5em", 
                        font_weight="bold", 
                        color="#333"),
                rx.text("Aquí va el contenido principal de la aplicación.", 
                        font_size="1em", 
                        color="#666",
                        text_align="center"),
                rx.text("El área se ajusta automáticamente al tamaño de la ventana.", 
                        font_size="0.9em", 
                        color="#888",
                        text_align="center"),
                spacing="2",
                align_items="center",
                justify_content="center",
                height="100%",
            ),
            background_color="white",
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

def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            header(),
            main_content_area(),
            width="90vw",
            height="90vh",
            border="2px solid #2979FF",  # Azul puro y fino
            border_radius="15px",
            spacing="1",
            overflow="hidden",
        ),
        width="100vw",
        height="100vh",
        display="flex",
        align_items="center",
        justify_content="center",
        background="#fff",  # Fondo exterior blanco puro
        margin="0",
        padding="0",
    )

app = rx.App(
    theme=rx.theme(
        accent_color="violet",
        gray_color="slate",
        styles={
            "*": {
                "margin": "0",
                "padding": "0",
                "boxSizing": "border-box",
            },
            "html, body": {
                "height": "100%",
                "width": "100%",
                "overflow": "hidden",
                "fontFamily": "system-ui, -apple-system, sans-serif",
            },
            "body": {
                "&::-webkit-scrollbar": {
                    "display": "none",
                },
                "scrollbarWidth": "none",
                "msOverflowStyle": "none",
            },
        },
    ),
)
app.add_page(index)
