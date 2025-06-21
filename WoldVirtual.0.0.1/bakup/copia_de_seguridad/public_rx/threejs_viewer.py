"""
Placeholder para la integración del visor 3D basado en React/Three.js.
Aquí se integrará el componente frontend avanzado en el futuro.
"""

import reflex as rx

class ThreejsViewer(rx.Component):
    library = "frontend_react_threejs/Complemento_react_reflex/bk_public/src/ThreeCanvas"
    tag = "ThreeCanvas"
    sceneData: dict = None
    on_event: rx.EventHandler = None  # Handler para eventos desde React, sin argumentos


def threejs_viewer(sceneData=None, on_event=None, **props):
    """Instancia el visor 3D con props y handler de eventos."""
    return ThreejsViewer.create(sceneData=sceneData, on_event=on_event, **props) 