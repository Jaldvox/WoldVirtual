"""Componente de la página de inicio."""
import reflex as rx
from .scene3d import Scene3D

def home() -> rx.Component:
    """Renderiza la página de inicio."""
    return rx.vstack(
        # Hero section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Bienvenido a WoldVirtual",
                    size="2xl",
                    color="white",
                    text_align="center",
                ),
                rx.text(
                    "El primer metaverso 3D descentralizado",
                    color="white",
                    text_align="center",
                ),
                rx.button(
                    "Explorar Ahora",
                    size="lg",
                    color_scheme="blue",
                    margin_top="4",
                ),
                spacing="4",
                padding="8",
            ),
            width="100%",
            height="100vh",
            background="linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/hero-bg.jpg')",
            background_size="cover",
            background_position="center",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        
        # Características principales
        rx.box(
            rx.vstack(
                rx.heading("Características Principales", size="xl", margin_bottom="8"),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.icon("cube", size="4xl", color="blue.500"),
                            rx.heading("Escenas 3D", size="md"),
                            rx.text("Crea y explora escenas 3D inmersivas"),
                            align="center",
                            spacing="4",
                        ),
                        padding="6",
                        border_radius="lg",
                        background="white",
                        shadow="lg",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.icon("wallet", size="4xl", color="green.500"),
                            rx.heading("NFTs", size="md"),
                            rx.text("Compra y vende activos digitales únicos"),
                            align="center",
                            spacing="4",
                        ),
                        padding="6",
                        border_radius="lg",
                        background="white",
                        shadow="lg",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.icon("users", size="4xl", color="purple.500"),
                            rx.heading("Comunidad", size="md"),
                            rx.text("Conecta con otros creadores y coleccionistas"),
                            align="center",
                            spacing="4",
                        ),
                        padding="6",
                        border_radius="lg",
                        background="white",
                        shadow="lg",
                    ),
                    spacing="8",
                    justify="center",
                ),
                padding="16",
                width="100%",
            ),
            background="gray.50",
        ),
        
        # Vista previa 3D
        rx.box(
            rx.vstack(
                rx.heading("Explora el Metaverso", size="xl", margin_bottom="8"),
                Scene3D(),
                padding="16",
                width="100%",
            ),
            background="white",
        ),
        
        # Llamada a la acción
        rx.box(
            rx.vstack(
                rx.heading(
                    "¿Listo para comenzar?",
                    size="xl",
                    color="white",
                    text_align="center",
                ),
                rx.text(
                    "Únete a nuestra comunidad y comienza a crear",
                    color="white",
                    text_align="center",
                ),
                rx.button(
                    "Crear Cuenta",
                    size="lg",
                    color_scheme="blue",
                    margin_top="4",
                ),
                spacing="4",
                padding="16",
            ),
            width="100%",
            background="linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('/cta-bg.jpg')",
            background_size="cover",
            background_position="center",
        ),
        
        width="100%",
        spacing="0",
    ) 