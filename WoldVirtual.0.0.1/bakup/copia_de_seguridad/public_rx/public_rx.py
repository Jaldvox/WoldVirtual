import reflex as rx
from rxconfig import config

class State(rx.State):
    """El estado de la aplicación."""
    show_networks_menu: bool = False
    selected_network: str = "Redes Blockchain"

    def toggle_networks_menu(self):
        self.show_networks_menu = not self.show_networks_menu

    def select_network(self, network: str):
        self.selected_network = network
        self.show_networks_menu = False

# Definimos colores para consistencia con la imagen
COLOR_HEADER_BACKGROUND = "#FFD700"  # Amarillo dorado
COLOR_MAIN_GREEN_BACKGROUND = "#3CB371" # Verde medio (verde primavera marino)
COLOR_OUTER_BORDER = "#0000CD" # Azul medio (azul real)

def header() -> rx.Component:
    """Header amarillo como en la imagen de referencia."""
    return rx.hstack(
        # Logo y título
        rx.text(
            "World Virtual",
            font_size="1.1em",
            color="black",
            font_weight="bold"
        ),

        rx.spacer(),

        # Navegación
        rx.text("Mapa del proyecto.", font_size="0.8em", color="black", margin_x="0.5em"),
        rx.text("Libro blanco", font_size="0.8em", color="black", margin_x="0.5em"),
        rx.text("Código abierto", font_size="0.8em", color="black", margin_x="0.5em"),

        # Selector de red (envuelto en un rx.box para posicionamiento relativo del dropdown)
        rx.box(
            rx.button(
                State.selected_network,
                on_click=State.toggle_networks_menu,
                bg="#343a40",
                color="white",
                font_size="0.65em",
                padding="0.3em 0.6em",
                border_radius="4px",
                cursor="pointer",
            ),

            # Dropdown menu
            rx.cond(
                State.show_networks_menu,
                rx.box( # Este box es el contenedor del vstack para el dropdown
                    rx.vstack(
                        rx.button("Binance Smart Chain", on_click=lambda: State.select_network("Binance Smart Chain"),
                                  font_size="0.7em", width="100%", padding="0.3em 0.6em",
                                  bg="white", border_radius="0", _hover={"bg": "#f0f0f0"}),
                        rx.button("Ethereum", on_click=lambda: State.select_network("Ethereum"),
                                  font_size="0.7em", width="100%", padding="0.3em 0.6em",
                                  bg="white", border_radius="0", _hover={"bg": "#f0f0f0"}),
                        rx.button("Polygon", on_click=lambda: State.select_network("Polygon"),
                                  font_size="0.7em", width="100%", padding="0.3em 0.6em",
                                  bg="white", border_radius="0", _hover={"bg": "#f0f0f0"}),
                        rx.button("Avalanche", on_click=lambda: State.select_network("Avalanche"),
                                  font_size="0.7em", width="100%", padding="0.3em 0.6em",
                                  bg="white", border_radius="0", _hover={"bg": "#f0f0f0"}),
                        rx.button("Arbitrum", on_click=lambda: State.select_network("Arbitrum"),
                                  font_size="0.7em", width="100%", padding="0.3em 0.6em",
                                  bg="white", border_radius="0", _hover={"bg": "#f0f0f0"}),
                        rx.button("Solana", on_click=lambda: State.select_network("Solana"),
                                  font_size="0.7em", width="100%", padding="0.3em 0.6em",
                                  bg="white", border_radius="0", _hover={"bg": "#f0f0f0"}),
                        spacing="0", # Elimina espacio entre los botones del dropdown
                        align_items="start",
                    ),
                    position="absolute",
                    # Calcula la posición justo debajo del botón. 50px es la altura del header.
                    # top="calc(100% + 5px)" sería relativo al parent si el parent fuera el botón.
                    # Aquí, es relativo al box que contiene el botón y el dropdown.
                    top="40px", # Coloca el dropdown 40px desde la parte superior del box padre.
                    right="0",
                    background_color="white",
                    border="1px solid #ddd",
                    border_radius="6px",
                    box_shadow="0 2px 8px rgba(0,0,0,0.1)",
                    width="160px",
                    z_index="1000",
                    padding="0.5em 0", # Pequeño padding vertical para el contenido del dropdown
                ),
                rx.fragment() # Cuando show_networks_menu es False, renderiza un fragmento vacío
            ),
            position="relative", # Este box es el que contiene el botón y el dropdown, y necesita ser relativo.
        ),

        width="100%",
        height="50px",
        background_color=COLOR_HEADER_BACKGROUND,
        padding_x="1em",
        align_items="center",
        position="relative", # Necesario para que los elementos hijos con position: absolute se posicionen correctamente
    )

def main_content() -> rx.Component:
    """Área de contenido principal con fondo verde y caja blanca central."""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.text(
                    "Área de Contenido Principal",
                    font_weight="bold",
                    font_size="1.5em",
                    color="#333"
                ),
                rx.text(
                    "Aquí va el contenido principal de la aplicación.",
                    color="#666",
                    text_align="center"
                ),
                rx.text(
                    "El área se ajusta automáticamente al tamaño de la ventana.",
                    color="#888",
                    font_size="0.9em",
                    text_align="center"
                ),
                align="center",
                spacing="4",
                width="100%", # Asegura que el vstack ocupe todo el ancho disponible en el box padre
            ),
            background_color="white",
            border_radius="16px",
            # ¡Aquí quitamos el borde de la caja blanca interior para que coincida con la imagen!
            # border=f"1px solid {BORDER_COLOR}", # Descomenta si quieres un borde interno.
            box_shadow="0 4px 15px rgba(0,0,0,0.1)", # Sombra para dar profundidad sin borde
            width="90%", # Ajuste del tamaño de la caja blanca dentro del área verde
            height="90%",
            padding="2em",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        width="100%",
        height="100%",
        background_color=COLOR_MAIN_GREEN_BACKGROUND, # Verde del fondo principal
        padding="1em", # Pequeño padding alrededor de la caja blanca dentro del área verde
    )

def app_layout() -> rx.Component:
    """Contenedor principal de la aplicación con el marco azul exterior."""
    return rx.center(
        rx.vstack(
            header(),
            main_content(),
            spacing="0", # Elimina el espacio entre el header y el contenido principal
            # Marco azul muy pequeñito como en la imagen
            border=f"1px solid {COLOR_OUTER_BORDER}", # El marco azul exterior, muy fino (1px)
            border_radius="12px", # Radio de las esquinas del marco exterior
            overflow="hidden", # Asegura que el contenido y los bordes redondeados se comporten bien
            # Ajuste de tamaño para que el marco exterior se vea "pequeñito" alrededor de la app.
            # Incrementado ligeramente para permitir más espacio verde visible.
            width="96vw",
            height="96vh",
            background_color=COLOR_MAIN_GREEN_BACKGROUND, # Fondo del marco principal (detrás del header/contenido)
        ),
        width="100vw",
        height="100vh",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)", # Fondo degradado
    )

# Configuración de la aplicación
app = rx.App(
    theme=rx.theme(
        accent_color="blue",
        gray_color="slate",
        styles={
            "*": {
                "margin": "0",
                "padding": "0",
                "box_sizing": "border-box", # Corregido a snake_case
            },
            "html, body": {
                "height": "100%",
                "width": "100%",
                "font_family": "system-ui, -apple-system, sans-serif", # Corregido a snake_case
                "line_height": "1.5",
            },
            "body": {
                "&::-webkit-scrollbar": {
                    "display": "none",
                },
                "scrollbar_width": "none", # Corregido a snake_case
                "ms_overflow_style": "none", # Corregido a snake_case
            },
        },
    ),
)

app.add_page(app_layout, route="/") # Cambiado a app_layout para mayor claridad