"""Componente de la barra de navegación."""
import reflex as rx
from ..state import State

def navbar() -> rx.Component:
    """Renderiza la barra de navegación."""
    return rx.box(
        rx.hstack(
            # Logo y nombre
            rx.hstack(
                rx.image(src="/logo.png", width="40px", height="40px"),
                rx.heading("WoldVirtual", size="md"),
                spacing="4",
            ),
            
            # Enlaces de navegación
            rx.hstack(
                rx.link("Inicio", href="/", color="white"),
                rx.link("Explorar", href="/explore", color="white"),
                rx.link("Crear", href="/create", color="white"),
                rx.link("Mercado", href="/marketplace", color="white"),
                spacing="6",
            ),
            
            # Botones de autenticación
            rx.hstack(
                rx.cond(
                    State.is_connected,
                    rx.hstack(
                        rx.text(State.wallet_address[:6] + "..." + State.wallet_address[-4:]),
                        rx.button("Desconectar", on_click=State.disconnect_wallet),
                        spacing="4",
                    ),
                    rx.button("Conectar Billetera", on_click=State.connect_wallet),
                ),
                spacing="4",
            ),
            
            justify="space-between",
            padding="4",
            width="100%",
            background="rgba(0, 0, 0, 0.8)",
            backdrop_filter="blur(10px)",
            position="fixed",
            top="0",
            z_index="1000",
        ),
    ) 