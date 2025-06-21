import reflex as rx

class State(rx.State):
    """Estado global de la app."""
    show_networks_menu: bool = False
    selected_network: str = "Redes Blockchain"
    usuario: str = "Invitado"

    def toggle_networks_menu(self):
        self.show_networks_menu = not self.show_networks_menu

    def select_network(self, network: str):
        self.selected_network = network
        self.show_networks_menu = False 