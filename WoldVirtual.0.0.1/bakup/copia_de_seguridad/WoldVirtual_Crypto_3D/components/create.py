"""Componente de la página de creación."""
import reflex as rx
from ..state import State
from .scene3d import Scene3D

def create() -> rx.Component:
    """Renderiza la página de creación."""
    return rx.hstack(
        # Panel de herramientas
        rx.box(
            rx.vstack(
                rx.heading("Herramientas", size="md", margin_bottom="4"),
                
                # Herramientas de transformación
                rx.vstack(
                    rx.heading("Transformación", size="sm"),
                    rx.hstack(
                        rx.button("Mover", on_click=State.set_tool("move")),
                        rx.button("Rotar", on_click=State.set_tool("rotate")),
                        rx.button("Escalar", on_click=State.set_tool("scale")),
                        spacing="2",
                    ),
                    spacing="2",
                ),
                
                # Herramientas de modelado
                rx.vstack(
                    rx.heading("Modelado", size="sm"),
                    rx.hstack(
                        rx.button("Cubo", on_click=State.add_primitive("cube")),
                        rx.button("Esfera", on_click=State.add_primitive("sphere")),
                        rx.button("Cilindro", on_click=State.add_primitive("cylinder")),
                        spacing="2",
                    ),
                    spacing="2",
                ),
                
                # Herramientas de iluminación
                rx.vstack(
                    rx.heading("Iluminación", size="sm"),
                    rx.hstack(
                        rx.button("Punto", on_click=State.add_light("point")),
                        rx.button("Direccional", on_click=State.add_light("directional")),
                        rx.button("Spot", on_click=State.add_light("spot")),
                        spacing="2",
                    ),
                    spacing="2",
                ),
                
                # Propiedades del objeto seleccionado
                rx.cond(
                    State.selected_object,
                    rx.vstack(
                        rx.heading("Propiedades", size="sm"),
                        rx.input(
                            placeholder="Nombre",
                            value=State.selected_object.name,
                            on_change=State.update_object_name,
                        ),
                        rx.hstack(
                            rx.text("X:"),
                            rx.number_input(
                                value=State.selected_object.position.x,
                                on_change=lambda x: State.update_object_position("x", x),
                            ),
                            rx.text("Y:"),
                            rx.number_input(
                                value=State.selected_object.position.y,
                                on_change=lambda y: State.update_object_position("y", y),
                            ),
                            rx.text("Z:"),
                            rx.number_input(
                                value=State.selected_object.position.z,
                                on_change=lambda z: State.update_object_position("z", z),
                            ),
                            spacing="2",
                        ),
                        spacing="2",
                    ),
                ),
                
                # Botones de acción
                rx.vstack(
                    rx.button(
                        "Guardar Escena",
                        color_scheme="blue",
                        width="100%",
                        on_click=State.save_scene,
                    ),
                    rx.button(
                        "Exportar",
                        color_scheme="green",
                        width="100%",
                        on_click=State.export_scene,
                    ),
                    spacing="2",
                ),
                
                spacing="6",
                padding="4",
                width="300px",
                height="100vh",
                background="white",
                shadow="md",
            ),
        ),
        
        # Área de edición 3D
        rx.box(
            Scene3D(),
            flex="1",
            height="100vh",
        ),
        
        width="100%",
        spacing="0",
    ) 