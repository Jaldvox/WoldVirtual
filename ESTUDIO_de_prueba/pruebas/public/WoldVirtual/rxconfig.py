import reflex as rx

config = rx.Config(
    app_name="WoldVirtual",
    
    # Puertos de desarrollo
    frontend_port=3000,
    backend_port=8000,
    
    # Base de datos
    db_url="sqlite:///reflex.db",
    
    # CORS para desarrollo
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Para React si lo usas
        "http://127.0.0.1:5173",
    ],
    
    # Plugins
    plugins=[
        rx.plugins.TailwindV3Plugin(),
    ],
    
    # Configuración de Tailwind personalizada
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "primary": "#00ff00",      # Verde neón (tu color)
                    "secondary": "#0099ff",    # Azul
                    "accent": "#ff6b35",       # Naranja
                    "dark": "#1a1a2e",        # Fondo oscuro
                    "darker": "#16213e",       # Más oscuro
                }
            }
        }
    }
)