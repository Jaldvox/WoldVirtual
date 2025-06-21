import reflex as rx

class State(rx.State):
    """Estado global de la aplicación: red seleccionada, usuario, menú de redes, etc."""
    show_networks_menu: bool = False
    selected_network: str = "Redes Blockchain"
    usuario: str = "Invitado"
    wallet_address: str = ""
    avatar_url: str = ""
    inventario: list = []
    ultimo_evento: str = None  # Guarda el último evento recibido desde React

    def toggle_networks_menu(self):
        """Alterna la visibilidad del menú de selección de red blockchain."""
        self.show_networks_menu = not self.show_networks_menu

    def select_network(self, network: str):
        """Selecciona una red blockchain y cierra el menú."""
        self.selected_network = network
        self.show_networks_menu = False

    # Métodos para gestión de usuario
    def login(self, usuario: str, wallet: str):
        self.usuario = usuario
        self.wallet_address = wallet

    def logout(self):
        self.usuario = "Invitado"
        self.wallet_address = ""
        self.avatar_url = ""
        self.inventario = []

    def handle_threejs_event(self):
        """Maneja eventos recibidos desde el visor 3D React/Three.js (sin datos)."""
        print("¡Evento recibido desde Three.js!")
        self.ultimo_evento = "Evento recibido (sin datos)" 