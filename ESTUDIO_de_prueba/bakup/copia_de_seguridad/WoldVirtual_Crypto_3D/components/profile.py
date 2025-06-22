import reflex as rx
 
class Profile(rx.Component):
    """Componente de perfil de usuario mínimo."""
    def render(self):
        return rx.text("Perfil de usuario (componente mínimo)") 