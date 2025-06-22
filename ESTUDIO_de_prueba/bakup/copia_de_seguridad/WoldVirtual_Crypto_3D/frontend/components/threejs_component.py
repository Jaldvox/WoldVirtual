import reflex as rx

# Placeholder: aquí iría la integración real con Three.js
# En Reflex, los custom components se pueden crear usando rx.Component.custom(...)

def ThreeJSViewer(scene: str):
    return rx.box(f"Three.js scene: {scene}", background_color="#222", color="white", padding="2em", border_radius="1em") 