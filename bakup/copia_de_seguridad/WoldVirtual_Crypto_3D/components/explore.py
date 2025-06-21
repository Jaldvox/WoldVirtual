"""Componente de la página de exploración."""
import reflex as rx
from ..state import State

def explore() -> rx.Component:
    """Renderiza la página de exploración."""
    return rx.vstack(
        # Filtros y búsqueda
        rx.box(
            rx.hstack(
                rx.input(
                    placeholder="Buscar escenas...",
                    width="300px",
                ),
                rx.select(
                    ["Todos", "Populares", "Recientes", "Mis Favoritos"],
                    placeholder="Filtrar por",
                    width="200px",
                ),
                rx.button("Buscar", color_scheme="blue"),
                spacing="4",
                padding="4",
            ),
            width="100%",
            background="white",
            shadow="sm",
        ),
        
        # Grid de escenas
        rx.box(
            rx.wrap(
                rx.foreach(
                    State.scenes,
                    lambda scene: rx.box(
                        rx.vstack(
                            rx.image(
                                src=scene.thumbnail_url or "/placeholder.jpg",
                                width="100%",
                                height="200px",
                                object_fit="cover",
                            ),
                            rx.vstack(
                                rx.heading(scene.name, size="md"),
                                rx.text(scene.description, no_of_lines=2),
                                rx.hstack(
                                    rx.text(f"Vistas: {scene.views}"),
                                    rx.text(f"Visitas: {scene.visits}"),
                                    spacing="4",
                                ),
                                rx.button(
                                    "Explorar",
                                    color_scheme="blue",
                                    width="100%",
                                ),
                                spacing="2",
                                padding="4",
                            ),
                            border_radius="lg",
                            background="white",
                            shadow="md",
                            width="300px",
                        ),
                    ),
                ),
                spacing="6",
                justify="center",
                padding="8",
            ),
            width="100%",
            background="gray.50",
        ),
        
        # Paginación
        rx.box(
            rx.hstack(
                rx.button("Anterior", is_disabled=State.current_page == 1),
                rx.text(f"Página {State.current_page} de {State.total_pages}"),
                rx.button("Siguiente", is_disabled=State.current_page == State.total_pages),
                spacing="4",
                padding="4",
            ),
            width="100%",
            background="white",
            shadow="sm",
        ),
        
        width="100%",
        spacing="0",
    ) 