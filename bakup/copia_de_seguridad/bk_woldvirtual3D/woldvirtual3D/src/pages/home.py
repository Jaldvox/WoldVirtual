"""
Página principal de Wold Virtual 3D
Página de inicio con información general y navegación
"""

from reflex import html, link
from components import Header, Footer, Navigation, Container, Card, Button


def HomePage():
    """Página principal de la aplicación"""
    
    # Datos de navegación
    nav_items = [
        {"text": "Inicio", "url": "/"},
        {"text": "Escena 3D", "url": "/3d-scene"},
        {"text": "Acerca de", "url": "/about"},
        {"text": "Dashboard", "url": "/dashboard"}
    ]
    
    # Datos de características
    features = [
        {
            "title": "Gráficos 3D Avanzados",
            "description": "Renderizado en tiempo real con Three.js y WebGL",
            "icon": "🎮"
        },
        {
            "title": "Interactividad Total",
            "description": "Controles intuitivos para explorar el mundo virtual",
            "icon": "🖱️"
        },
        {
            "title": "Rendimiento Optimizado",
            "description": "Experiencia fluida en todos los dispositivos",
            "icon": "⚡"
        },
        {
            "title": "Personalización",
            "description": "Crea y personaliza tu propio espacio virtual",
            "icon": "🎨"
        }
    ]
    
    return html.div(
        # Encabezado
        Header.main(
            title="Wold Virtual 3D",
            subtitle="Explora un mundo virtual inmersivo y personalizable",
            actions=[
                Button.primary("Comenzar", href="/3d-scene"),
                Button.secondary("Más Info", href="/about")
            ]
        ),
        
        # Navegación
        Navigation.main(
            items=nav_items,
            active_item="/"
        ),
        
        # Contenido principal
        Container.main([
            # Sección hero
            html.section(
                html.div(
                    html.div(
                        html.h1(
                            "Bienvenido a Wold Virtual 3D",
                            class_name="text-4xl font-bold text-gray-900 mb-4"
                        ),
                        html.p(
                            "Sumérgete en un mundo virtual completamente nuevo. Explora, crea y conecta en un espacio 3D inmersivo diseñado para la próxima generación de experiencias digitales.",
                            class_name="text-xl text-gray-600 mb-8 max-w-3xl"
                        ),
                        html.div(
                            Button.primary("Explorar Ahora", href="/3d-scene", size="large"),
                            class_name="flex space-x-4"
                        ),
                        class_name="text-center"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-gradient-to-r from-blue-50 to-indigo-100"
            ),
            
            # Sección de características
            html.section(
                html.div(
                    html.h2(
                        "Características Principales",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-12"
                    ),
                    html.div(
                        [
                            Card.basic(
                                title=feature["title"],
                                content=[
                                    html.div(
                                        feature["icon"],
                                        class_name="text-4xl mb-4"
                                    ),
                                    html.p(
                                        feature["description"],
                                        class_name="text-gray-600"
                                    )
                                ]
                            ) for feature in features
                        ],
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-white"
            ),
            
            # Sección de estadísticas
            html.section(
                html.div(
                    html.div(
                        [
                            html.div(
                                html.div(
                                    html.div(
                                        stat["number"],
                                        class_name="text-4xl font-bold text-blue-600"
                                    ),
                                    html.p(
                                        stat["label"],
                                        class_name="text-gray-600 mt-2"
                                    ),
                                    class_name="text-center"
                                ),
                                class_name="col-span-1"
                            ) for stat in [
                                {"number": "10K+", "label": "Usuarios Activos"},
                                {"number": "50+", "label": "Escenas Creadas"},
                                {"number": "99.9%", "label": "Tiempo Activo"},
                                {"number": "24/7", "label": "Soporte Disponible"}
                            ]
                        ],
                        class_name="grid grid-cols-2 md:grid-cols-4 gap-8"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-gray-50"
            ),
            
            # Sección CTA
            html.section(
                html.div(
                    html.div(
                        html.h2(
                            "¿Listo para comenzar?",
                            class_name="text-3xl font-bold text-white mb-4"
                        ),
                        html.p(
                            "Únete a miles de usuarios que ya están explorando el mundo virtual",
                            class_name="text-xl text-blue-100 mb-8"
                        ),
                        Button.primary("Crear Cuenta", href="/register", size="large"),
                        class_name="text-center"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-blue-600"
            )
        ]),
        
        # Pie de página
        Footer.main(
            links=[
                {"text": "Términos", "url": "/terms"},
                {"text": "Privacidad", "url": "/privacy"},
                {"text": "Contacto", "url": "/contact"}
            ]
        ),
        
        # Metadatos
        link(rel="stylesheet", href="/static/css/tailwind.css"),
        class_name="min-h-screen bg-gray-50"
    ) 