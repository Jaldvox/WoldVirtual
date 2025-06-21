"""Estilos globales de la aplicación."""
import reflex as rx

# Estilos base
BASE_STYLE = {
    "font_family": "system-ui, -apple-system, sans-serif",
    "background": "black",
    "color": "white",
}

# Estilos de la escena 3D
SCENE_STYLE = {
    "width": "100%",
    "height": "100%",
    "position": "absolute",
    "top": 0,
    "left": 0,
    "z_index": 0,
}

# Estilos de la UI
UI_STYLE = {
    "width": "100%",
    "height": "100%",
    "position": "absolute",
    "top": 0,
    "left": 0,
    "z_index": 1000,
    "pointer_events": "none",
}

# Estilos de los botones
BUTTON_STYLE = {
    "pointer_events": "auto",
    "background": "rgba(147, 51, 234, 0.8)",
    "color": "white",
    "border_radius": "md",
    "padding": "2",
    "hover": {
        "background": "rgba(147, 51, 234, 1)",
    },
} 