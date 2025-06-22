import reflex as rx

config = rx.Config(
    app_name="WoldVirtual_Crypto_3Dv1",
    plugins=[rx.plugins.TailwindV3Plugin()],
)

def integration_info() -> rx.Component:
    """Información de integración con el componente React."""
    return rx.vstack(
        rx.text(
            "🔗 Integración con React Component",
            font_size="1.2em",
            font_weight="bold",
            color=AppConfig.COLORS["text_secondary"]
        ),
        rx.text(
            "El componente React (ThreejsWebgl) se conectará aquí:",
            color=AppConfig.COLORS["text_muted"]
        ),
        rx.text(
            "• Backend: http://localhost:8000",
            color=AppConfig.COLORS["text_light"]
        ),
        rx.text(
            "• Frontend React: http://localhost:5173", 
            color=AppConfig.COLORS["text_light"]
        ),
        rx.text(
            "• WebSocket: ws://localhost:8000/ws",
            color=AppConfig.COLORS["text_light"]
        ),
        spacing="0.5em",
        margin_top="1em"
    )

def main_content() -> rx.Component:
    """Contenido principal optimizado para el metaverso 3D."""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.text(
                    "Metaverso Crypto 3D",
                    font_weight="bold",
                    font_size="1.8em",
                    color=AppConfig.COLORS["text_secondary"],
                    margin_bottom="1em"
                ),
                rx.text(
                    "Zona preparada para el componente React del metaverso cryptocurrency 3D",
                    color=AppConfig.COLORS["text_muted"],
                    text_align="center",
                    font_size="1.1em",
                    margin_bottom="2em"
                ),
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.text(
                                "🌐 Espacio reservado para Three.js / React 3D Component",
                                font_size="1.2em",
                                color=AppConfig.COLORS["text_light"],
                                text_align="center"
                            ),
                            integration_info(),  # Nueva función
                            spacing="1em"
                        ),
                        width="100%",
                        height="400px",
                        border=f"2px dashed {AppConfig.COLORS['text_light']}",
                        border_radius="12px",
                        background="linear-gradient(45deg, #f8f9fa 25%, transparent 25%), linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #f8f9fa 75%), linear-gradient(-45deg, transparent 75%, #f8f9fa 75%)",
                        background_size="20px 20px",
                        background_position="0 0, 0 10px, 10px -10px, -10px 0px"
                    ),
                    width="100%",
                    flex="1"
                ),
                align="center",
                spacing="0",
                width="100%",
                height="100%",
            ),
            background_color=AppConfig.COLORS["white"],
            border_radius=AppConfig.LAYOUT["content_border_radius"],
            box_shadow="0 8px 32px rgba(0,0,0,0.12)",
            width=AppConfig.LAYOUT["content_width"],
            height=AppConfig.LAYOUT["content_height"],
            padding="2em",
            display="flex",
            overflow="hidden",
        ),
        width="100%",
        height="100%",
        background_color=AppConfig.COLORS["main_bg"],
        padding=AppConfig.LAYOUT["green_padding"],
    )