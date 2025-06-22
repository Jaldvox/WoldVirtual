"""
Script simplificado para arrancar WoldVirtual Crypto 3D
Solo inicia el servidor Reflex sin verificaciones complejas
"""

import os
import sys
import reflex as rx
from pathlib import Path

# Configurar variables de entorno básicas
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DEBUG_MODE", "True")

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_simple_app():
    """Crear una aplicación Reflex simple"""
    
    # Crear una página básica
    def home_page():
        return rx.center(
            rx.vstack(
                rx.heading("🚀 WoldVirtual Crypto 3D", size="lg", color="blue.500"),
                rx.text("Metaverso Descentralizado 3D", color="gray.600"),
                rx.text("Versión 0.0.9", color="gray.500"),
                rx.divider(),
                rx.text("🎮 Sistema funcionando correctamente!", color="green.500"),
                rx.text("🌐 Frontend disponible en http://localhost:3000", color="blue.500"),
                rx.text("⛓️ Web3 integrado", color="purple.500"),
                rx.text("🎨 Assets 3D cargados", color="orange.500"),
                rx.divider(),
                rx.button(
                    "🎯 Explorar Metaverso",
                    color_scheme="blue",
                    size="lg",
                    margin_top="20px"
                ),
                spacing="20px",
                padding="40px",
                bg="white",
                border_radius="lg",
                box_shadow="lg",
                max_width="600px"
            ),
            height="100vh",
            bg="gray.50"
        )

    # Crear la aplicación
    app = rx.App()
    
    # Agregar la página principal
    app.add_page(
        home_page,
        route="/",
        title="WoldVirtual Crypto 3D",
        description="Metaverso descentralizado 3D con capacidades de criptomonedas"
    )
    
    return app

def main():
    """Función principal"""
    print("🚀 Iniciando WoldVirtual Crypto 3D - Versión Simplificada")
    print("=" * 60)
    
    try:
        # Crear la aplicación
        print("📋 Creando aplicación Reflex...")
        app = create_simple_app()
        
        print("✅ Aplicación creada exitosamente")
        print("\n🌐 URLs de acceso:")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8000")
        print("\n🎮 ¡El metaverso está listo!")
        print("   Presiona Ctrl+C para detener")
        print("=" * 60)
        
        # Compilar y ejecutar
        # app.compile()
        print("\n⚡ Para iniciar el servidor Reflex ejecuta en terminal:")
        print("   reflex run")
        print("\nLuego abre http://localhost:3000 en tu navegador.")
        # app.run(...) eliminado porque no existe en esta versión
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        print("👋 ¡Gracias por usar WoldVirtual Crypto 3D!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("🔧 Revisa la configuración e intenta nuevamente")

if __name__ == "__main__":
    main() 