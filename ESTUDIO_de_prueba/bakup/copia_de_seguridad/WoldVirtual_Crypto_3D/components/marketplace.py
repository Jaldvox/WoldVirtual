"""Componente de la página del marketplace."""
import reflex as rx
from ..state import State

def marketplace() -> rx.Component:
    """Renderiza la página del marketplace."""
    return rx.vstack(
        # Filtros y búsqueda
        rx.box(
            rx.hstack(
                rx.input(
                    placeholder="Buscar activos...",
                    width="300px",
                ),
                rx.select(
                    ["Todos", "Modelos 3D", "Texturas", "Escenas", "En Venta"],
                    placeholder="Categoría",
                    width="200px",
                ),
                rx.select(
                    ["Precio: Menor a Mayor", "Precio: Mayor a Menor", "Más Recientes", "Más Populares"],
                    placeholder="Ordenar por",
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
        
        # Grid de activos
        rx.box(
            rx.wrap(
                rx.foreach(
                    State.assets,
                    lambda asset: rx.box(
                        rx.vstack(
                            rx.image(
                                src=asset.thumbnail_url or "/placeholder.jpg",
                                width="100%",
                                height="200px",
                                object_fit="cover",
                            ),
                            rx.vstack(
                                rx.heading(asset.name, size="md"),
                                rx.text(asset.description, no_of_lines=2),
                                rx.hstack(
                                    rx.text(f"Tipo: {asset.asset_type}"),
                                    rx.text(f"Vistas: {asset.views}"),
                                    spacing="4",
                                ),
                                rx.hstack(
                                    rx.text(f"Precio: {asset.price} {asset.currency}"),
                                    rx.button(
                                        "Comprar",
                                        color_scheme="green",
                                        is_disabled=not asset.is_for_sale,
                                    ),
                                    spacing="4",
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
        
        # Modal de compra
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header("Confirmar Compra"),
                    rx.modal_body(
                        rx.vstack(
                            rx.text("¿Estás seguro de que deseas comprar este activo?"),
                            rx.text(f"Precio: {State.selected_asset.price} {State.selected_asset.currency}"),
                            spacing="4",
                        ),
                    ),
                    rx.modal_footer(
                        rx.button(
                            "Cancelar",
                            on_click=State.close_purchase_modal,
                        ),
                        rx.button(
                            "Confirmar Compra",
                            color_scheme="green",
                            on_click=State.purchase_asset,
                        ),
                        spacing="4",
                    ),
                ),
            ),
            is_open=State.show_purchase_modal,
        ),
        
        width="100%",
        spacing="0",
    ) 