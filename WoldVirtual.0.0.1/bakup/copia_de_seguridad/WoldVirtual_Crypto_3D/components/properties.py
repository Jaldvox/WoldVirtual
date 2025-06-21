"""Componente para el panel de propiedades."""
import reflex as rx
from typing import Dict, List, Optional
from ..state import State

def PropertiesPanel() -> rx.Component:
    """Renderiza el panel de propiedades."""
    return rx.vstack(
        # Propiedades generales
        rx.box(
            rx.vstack(
                rx.heading("Propiedades Generales", size="sm"),
                rx.vstack(
                    rx.hstack(
                        rx.text("Nombre:"),
                        rx.input(
                            value=State.selected_object.name if State.selected_object else "",
                            on_change=State.update_object_name,
                            is_disabled=not State.selected_object,
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Visible:"),
                        rx.switch(
                            is_checked=State.selected_object.visible if State.selected_object else True,
                            on_change=State.toggle_object_visibility,
                            is_disabled=not State.selected_object,
                        ),
                        spacing="2",
                    ),
                    spacing="2",
                ),
                spacing="2",
            ),
            padding="4",
            background="white",
            border_radius="md",
            shadow="sm",
        ),
        
        # Transformación
        rx.box(
            rx.vstack(
                rx.heading("Transformación", size="sm"),
                rx.vstack(
                    # Posición
                    rx.vstack(
                        rx.text("Posición", font_weight="bold"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("X"),
                                rx.number_input(
                                    value=State.selected_object.position.x if State.selected_object else 0,
                                    on_change=lambda x: State.update_object_position("x", x),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Y"),
                                rx.number_input(
                                    value=State.selected_object.position.y if State.selected_object else 0,
                                    on_change=lambda y: State.update_object_position("y", y),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Z"),
                                rx.number_input(
                                    value=State.selected_object.position.z if State.selected_object else 0,
                                    on_change=lambda z: State.update_object_position("z", z),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            spacing="2",
                        ),
                        spacing="2",
                    ),
                    
                    # Rotación
                    rx.vstack(
                        rx.text("Rotación", font_weight="bold"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("X"),
                                rx.number_input(
                                    value=State.selected_object.rotation.x if State.selected_object else 0,
                                    on_change=lambda x: State.update_object_rotation("x", x),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Y"),
                                rx.number_input(
                                    value=State.selected_object.rotation.y if State.selected_object else 0,
                                    on_change=lambda y: State.update_object_rotation("y", y),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Z"),
                                rx.number_input(
                                    value=State.selected_object.rotation.z if State.selected_object else 0,
                                    on_change=lambda z: State.update_object_rotation("z", z),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            spacing="2",
                        ),
                        spacing="2",
                    ),
                    
                    # Escala
                    rx.vstack(
                        rx.text("Escala", font_weight="bold"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("X"),
                                rx.number_input(
                                    value=State.selected_object.scale.x if State.selected_object else 1,
                                    on_change=lambda x: State.update_object_scale("x", x),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Y"),
                                rx.number_input(
                                    value=State.selected_object.scale.y if State.selected_object else 1,
                                    on_change=lambda y: State.update_object_scale("y", y),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Z"),
                                rx.number_input(
                                    value=State.selected_object.scale.z if State.selected_object else 1,
                                    on_change=lambda z: State.update_object_scale("z", z),
                                    is_disabled=not State.selected_object,
                                ),
                            ),
                            spacing="2",
                        ),
                        spacing="2",
                    ),
                    
                    spacing="4",
                ),
                spacing="2",
            ),
            padding="4",
            background="white",
            border_radius="md",
            shadow="sm",
        ),
        
        # Material
        rx.cond(
            State.selected_object and State.selected_object.material,
            rx.box(
                rx.vstack(
                    rx.heading("Material", size="sm"),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Color:"),
                            rx.color_picker(
                                value=State.selected_object.material.color,
                                on_change=State.update_material_color,
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.text("Metalness:"),
                            rx.slider(
                                value=State.selected_object.material.metalness,
                                on_change=State.update_material_metalness,
                                min=0,
                                max=1,
                                step=0.1,
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.text("Roughness:"),
                            rx.slider(
                                value=State.selected_object.material.roughness,
                                on_change=State.update_material_roughness,
                                min=0,
                                max=1,
                                step=0.1,
                            ),
                            spacing="2",
                        ),
                        spacing="2",
                    ),
                    spacing="2",
                ),
                padding="4",
                background="white",
                border_radius="md",
                shadow="sm",
            ),
        ),
        
        # Física
        rx.cond(
            State.selected_object and State.selected_object.physics,
            rx.box(
                rx.vstack(
                    rx.heading("Física", size="sm"),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Masa:"),
                            rx.number_input(
                                value=State.selected_object.physics.mass,
                                on_change=State.update_physics_mass,
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.text("Fricción:"),
                            rx.slider(
                                value=State.selected_object.physics.friction,
                                on_change=State.update_physics_friction,
                                min=0,
                                max=1,
                                step=0.1,
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.text("Restitución:"),
                            rx.slider(
                                value=State.selected_object.physics.restitution,
                                on_change=State.update_physics_restitution,
                                min=0,
                                max=1,
                                step=0.1,
                            ),
                            spacing="2",
                        ),
                        spacing="2",
                    ),
                    spacing="2",
                ),
                padding="4",
                background="white",
                border_radius="md",
                shadow="sm",
            ),
        ),
        
        spacing="4",
        padding="4",
        width="300px",
        height="100vh",
        background="gray.100",
        position="fixed",
        right=0,
        top=0,
        z_index=1000,
    ) 