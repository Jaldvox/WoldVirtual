"""
Páginas principales de WoldVirtual Crypto 3D.
Define las rutas y componentes de la interfaz de usuario.
"""

import reflex as rx
from typing import List, Dict, Any
from state import WoldVirtualState
from components.navbar import Navbar
from components.scene3d import Scene3D
from components.marketplace import Marketplace
from components.profile import Profile
from components.explore import Explore
from components.create import Create
from components.home import Home

# =============================================================================
# COMPONENTES DE LAYOUT
# =============================================================================

def LoadingScreen() -> rx.Component:
    """Pantalla de carga."""
    return rx.center(
        rx.vstack(
            rx.spinner(
                color="primary.500",
                size="lg",
                thickness="4px",
            ),
            rx.text(
                "Cargando WoldVirtual Crypto 3D...",
                font_size="lg",
                color="gray.600",
                margin_top="4",
            ),
            rx.progress(
                value=WoldVirtualState.get_loading_progress,
                width="300px",
                margin_top="4",
            ),
            spacing="4",
            align="center",
        ),
        width="100vw",
        height="100vh",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    )

def ErrorBoundary() -> rx.Component:
    """Componente para manejar errores."""
    return rx.center(
        rx.vstack(
            rx.icon(
                "warning",
                size="4xl",
                color="red.500",
            ),
            rx.heading(
                "¡Ups! Algo salió mal",
                size="lg",
                color="gray.800",
            ),
            rx.text(
                "Ha ocurrido un error inesperado. Por favor, recarga la página.",
                color="gray.600",
                text_align="center",
            ),
            rx.button(
                "Recargar Página",
                on_click=rx.window.location.reload,
                color_scheme="blue",
                margin_top="4",
            ),
            spacing="4",
            align="center",
            padding="8",
        ),
        width="100vw",
        height="100vh",
        background="gray.50",
    )

def Sidebar() -> rx.Component:
    """Barra lateral de navegación."""
    return rx.drawer(
        rx.drawer_overlay(),
        rx.drawer_content(
            rx.drawer_header(
                rx.hstack(
                    rx.heading("WoldVirtual", size="md"),
                    rx.spacer(),
                    rx.button(
                        rx.icon("close"),
                        on_click=WoldVirtualState.toggle_sidebar,
                        variant="ghost",
                        size="sm",
                    ),
                ),
            ),
            rx.drawer_body(
                rx.vstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("home"),
                            rx.text("Inicio"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("home"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("explore"),
                            rx.text("Explorar"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("explore"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("add"),
                            rx.text("Crear"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("create"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("store"),
                            rx.text("Marketplace"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("marketplace"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("person"),
                            rx.text("Perfil"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("profile"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    rx.divider(),
                    rx.text(
                        "Configuración",
                        font_size="sm",
                        color="gray.500",
                        font_weight="bold",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("settings"),
                            rx.text("Ajustes"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("settings"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("help"),
                            rx.text("Ayuda"),
                        ),
                        on_click=lambda: WoldVirtualState.navigate_to("help"),
                        variant="ghost",
                        width="100%",
                        justify="start",
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
            ),
            bg="white",
        ),
        is_open=WoldVirtualState.sidebar_open,
        placement="left",
        size="md",
    )

def Notifications() -> rx.Component:
    """Panel de notificaciones."""
    return rx.cond(
        WoldVirtualState.error_message != "" | WoldVirtualState.success_message != "",
        rx.toast(
            rx.toast_overlay(),
            rx.toast_title(
                rx.cond(
                    WoldVirtualState.error_message != "",
                    "Error",
                    "Éxito"
                ),
            ),
            rx.toast_description(
                rx.cond(
                    WoldVirtualState.error_message != "",
                    WoldVirtualState.error_message,
                    WoldVirtualState.success_message,
                ),
            ),
            rx.toast_close_button(),
            status=rx.cond(
                WoldVirtualState.error_message != "",
                "error",
                "success"
            ),
            duration=5000,
            on_close=WoldVirtualState.clear_messages,
        ),
        rx.fragment(),
    )

def NetworkStatus() -> rx.Component:
    """Indicador de estado de red."""
    return rx.hstack(
        rx.icon(
            rx.cond(
                WoldVirtualState.network_connected,
                "wifi",
                "wifi_off"
            ),
            color=rx.cond(
                WoldVirtualState.network_connected,
                "green.500",
                "red.500"
            ),
            size="sm",
        ),
        rx.text(
            rx.cond(
                WoldVirtualState.network_connected,
                f"{WoldVirtualState.network_latency}ms",
                "Desconectado"
            ),
            font_size="xs",
            color="gray.600",
        ),
        spacing="1",
        padding="2",
        background="white",
        border_radius="md",
        box_shadow="sm",
    )

# =============================================================================
# PÁGINA PRINCIPAL
# =============================================================================

def MainPage() -> rx.Component:
    """Página principal de la aplicación."""
    return rx.box(
        # Barra de navegación
        Navbar(),
        
        # Contenido principal
        rx.cond(
            WoldVirtualState.loading,
            LoadingScreen(),
            rx.box(
                rx.cond(
                    WoldVirtualState.current_page == "home",
                    Home(),
                    rx.cond(
                        WoldVirtualState.current_page == "explore",
                        Explore(),
                        rx.cond(
                            WoldVirtualState.current_page == "create",
                            Create(),
                            rx.cond(
                                WoldVirtualState.current_page == "marketplace",
                                Marketplace(),
                                rx.cond(
                                    WoldVirtualState.current_page == "profile",
                                    Profile(),
                                    rx.cond(
                                        WoldVirtualState.current_page == "scene",
                                        Scene3D(),
                                        Home(),  # Página por defecto
                                    )
                                )
                            )
                        )
                    )
                ),
                width="100%",
                height="calc(100vh - 60px)",
                overflow="hidden",
            )
        ),
        
        # Barra lateral
        Sidebar(),
        
        # Notificaciones
        Notifications(),
        
        # Indicador de red
        rx.positioned(
            NetworkStatus(),
            top="70px",
            right="20px",
            z_index="1000",
        ),
        
        # Configuración de tema
        background=rx.cond(
            WoldVirtualState.theme == "dark",
            "gray.900",
            "gray.50"
        ),
        color=rx.cond(
            WoldVirtualState.theme == "dark",
            "white",
            "black"
        ),
        width="100vw",
        height="100vh",
        overflow="hidden",
    )

# =============================================================================
# PÁGINA DE ESCENA 3D
# =============================================================================

def ScenePage() -> rx.Component:
    """Página de escena 3D."""
    return rx.box(
        rx.hstack(
            # Panel de controles
            rx.vstack(
                rx.heading(
                    WoldVirtualState.current_scene_name,
                    size="md",
                    margin_bottom="4",
                ),
                rx.divider(),
                
                # Controles de cámara
                rx.vstack(
                    rx.text("Cámara", font_weight="bold"),
                    rx.button(
                        "Vista Frontal",
                        on_click=lambda: WoldVirtualState.update_camera([0, 0, 10], [0, 0, 0]),
                        size="sm",
                        width="100%",
                    ),
                    rx.button(
                        "Vista Superior",
                        on_click=lambda: WoldVirtualState.update_camera([0, 10, 0], [0, 0, 0]),
                        size="sm",
                        width="100%",
                    ),
                    rx.button(
                        "Vista Lateral",
                        on_click=lambda: WoldVirtualState.update_camera([10, 0, 0], [0, 0, 0]),
                        size="sm",
                        width="100%",
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                
                rx.divider(),
                
                # Controles de iluminación
                rx.vstack(
                    rx.text("Iluminación", font_weight="bold"),
                    rx.switch(
                        "Sombras",
                        is_checked=WoldVirtualState.scene_settings["shadows_enabled"],
                        on_change=lambda value: WoldVirtualState.update_scene_settings({"shadows_enabled": value}),
                    ),
                    rx.switch(
                        "Niebla",
                        is_checked=WoldVirtualState.scene_settings["fog_enabled"],
                        on_change=lambda value: WoldVirtualState.update_scene_settings({"fog_enabled": value}),
                    ),
                    rx.switch(
                        "Post-procesamiento",
                        is_checked=WoldVirtualState.scene_settings["post_processing"],
                        on_change=lambda value: WoldVirtualState.update_scene_settings({"post_processing": value}),
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                
                rx.divider(),
                
                # Lista de assets
                rx.vstack(
                    rx.text("Assets en Escena", font_weight="bold"),
                    rx.text(
                        f"{WoldVirtualState.get_scene_asset_count()} assets cargados",
                        font_size="sm",
                        color="gray.600",
                    ),
                    rx.foreach(
                        WoldVirtualState.loaded_assets,
                        lambda asset: rx.hstack(
                            rx.text(asset["id"], font_size="sm"),
                            rx.spacer(),
                            rx.button(
                                "Remover",
                                size="xs",
                                color_scheme="red",
                                on_click=lambda aid=asset["id"]: WoldVirtualState.remove_asset(aid),
                            ),
                            width="100%",
                        )
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                
                spacing="4",
                width="300px",
                height="100%",
                padding="4",
                background="white",
                border_right="1px solid",
                border_color="gray.200",
                overflow_y="auto",
            ),
            
            # Área de renderizado 3D
            rx.box(
                Scene3D(),
                flex="1",
                height="100%",
                background="black",
            ),
            
            width="100%",
            height="100%",
        ),
        width="100%",
        height="100%",
    )

# =============================================================================
# PÁGINA DE CONFIGURACIÓN
# =============================================================================

def SettingsPage() -> rx.Component:
    """Página de configuración."""
    return rx.center(
        rx.vstack(
            rx.heading("Configuración", size="lg"),
            
            # Configuración de tema
            rx.vstack(
                rx.text("Tema", font_weight="bold"),
                rx.hstack(
                    rx.button(
                        "Claro",
                        on_click=lambda: WoldVirtualState.change_theme("light"),
                        color_scheme=rx.cond(
                            WoldVirtualState.theme == "light",
                            "blue",
                            "gray"
                        ),
                    ),
                    rx.button(
                        "Oscuro",
                        on_click=lambda: WoldVirtualState.change_theme("dark"),
                        color_scheme=rx.cond(
                            WoldVirtualState.theme == "dark",
                            "blue",
                            "gray"
                        ),
                    ),
                    spacing="2",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            
            rx.divider(),
            
            # Configuración de idioma
            rx.vstack(
                rx.text("Idioma", font_weight="bold"),
                rx.select(
                    ["Español", "English", "Português"],
                    placeholder="Seleccionar idioma",
                    value=WoldVirtualState.language,
                    on_change=lambda value: WoldVirtualState.change_language(value),
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            
            rx.divider(),
            
            # Configuración de notificaciones
            rx.vstack(
                rx.text("Notificaciones", font_weight="bold"),
                rx.switch(
                    "Habilitar notificaciones",
                    is_checked=WoldVirtualState.notifications_enabled,
                    on_change=lambda value: setattr(WoldVirtualState, "notifications_enabled", value),
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            
            rx.divider(),
            
            # Configuración de rendimiento
            rx.vstack(
                rx.text("Rendimiento", font_weight="bold"),
                rx.select(
                    ["Bajo", "Medio", "Alto", "Ultra"],
                    placeholder="Calidad gráfica",
                    value=WoldVirtualState.user_settings["performance"]["graphics_quality"],
                    on_change=lambda value: WoldVirtualState.update_user_profile({
                        "user_settings": {
                            **WoldVirtualState.user_settings,
                            "performance": {
                                **WoldVirtualState.user_settings["performance"],
                                "graphics_quality": value
                            }
                        }
                    }),
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            
            spacing="6",
            width="100%",
            max_width="600px",
            padding="8",
            background="white",
            border_radius="lg",
            box_shadow="lg",
        ),
        width="100%",
        height="100%",
        padding="4",
    )

# =============================================================================
# PÁGINA DE AYUDA
# =============================================================================

def HelpPage() -> rx.Component:
    """Página de ayuda."""
    return rx.center(
        rx.vstack(
            rx.heading("Centro de Ayuda", size="lg"),
            
            rx.accordion(
                rx.accordion_item(
                    rx.accordion_button("¿Cómo conectar mi wallet?"),
                    rx.accordion_panel(
                        "Para conectar tu wallet, haz clic en el botón 'Conectar Wallet' en la barra de navegación. "
                        "Se abrirá una ventana para seleccionar tu proveedor de wallet preferido."
                    ),
                ),
                rx.accordion_item(
                    rx.accordion_button("¿Cómo crear una escena 3D?"),
                    rx.accordion_panel(
                        "Ve a la sección 'Crear' y selecciona 'Nueva Escena'. "
                        "Puedes personalizar la configuración y agregar assets desde tu biblioteca."
                    ),
                ),
                rx.accordion_item(
                    rx.accordion_button("¿Cómo comprar assets en el marketplace?"),
                    rx.accordion_panel(
                        "Navega al marketplace, selecciona el asset que deseas comprar y haz clic en 'Comprar'. "
                        "Confirma la transacción en tu wallet."
                    ),
                ),
                rx.accordion_item(
                    rx.accordion_button("¿Cómo optimizar el rendimiento?"),
                    rx.accordion_panel(
                        "Ve a Configuración > Rendimiento y ajusta la calidad gráfica según tu dispositivo. "
                        "También puedes deshabilitar efectos opcionales."
                    ),
                ),
                allow_multiple=True,
                width="100%",
            ),
            
            rx.divider(),
            
            rx.hstack(
                rx.text("¿Necesitas más ayuda?"),
                rx.link(
                    "Contactar Soporte",
                    href="mailto:support@woldvirtual.com",
                    color="blue.500",
                ),
                spacing="2",
            ),
            
            spacing="6",
            width="100%",
            max_width="800px",
            padding="8",
            background="white",
            border_radius="lg",
            box_shadow="lg",
        ),
        width="100%",
        height="100%",
        padding="4",
    )

# =============================================================================
# RUTAS DE LA APLICACIÓN
# =============================================================================

# Configuración de rutas
app = rx.App(
    state=WoldVirtualState,
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
    ),
)

# Ruta principal
app.add_page(
    MainPage,
    route="/",
    title="WoldVirtual Crypto 3D",
    description="Metaverso descentralizado 3D con capacidades de criptomonedas",
)

# Rutas específicas
app.add_page(
    ScenePage,
    route="/scene",
    title="Escena 3D - WoldVirtual",
)

app.add_page(
    SettingsPage,
    route="/settings",
    title="Configuración - WoldVirtual",
)

app.add_page(
    HelpPage,
    route="/help",
    title="Ayuda - WoldVirtual",
)

# Configuración de la aplicación
app.compile() 