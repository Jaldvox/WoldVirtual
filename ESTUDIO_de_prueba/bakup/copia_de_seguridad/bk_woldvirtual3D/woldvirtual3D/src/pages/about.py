"""
Página Acerca de Wold Virtual 3D
Información sobre el proyecto y el equipo
"""

from reflex import html, link
from components import Header, Footer, Navigation, Container, Card, Button


def AboutPage():
    """Página de información sobre la aplicación"""
    
    # Datos de navegación
    nav_items = [
        {"text": "Inicio", "url": "/"},
        {"text": "Escena 3D", "url": "/3d-scene"},
        {"text": "Acerca de", "url": "/about"},
        {"text": "Dashboard", "url": "/dashboard"}
    ]
    
    # Datos del equipo
    team_members = [
        {
            "name": "Equipo de Desarrollo",
            "role": "Desarrollo Full-Stack",
            "description": "Especialistas en React, Three.js y Python",
            "avatar": "👨‍💻"
        },
        {
            "name": "Equipo de Diseño",
            "role": "UX/UI Design",
            "description": "Creadores de experiencias inmersivas",
            "avatar": "🎨"
        },
        {
            "name": "Equipo de Innovación",
            "role": "Investigación y Desarrollo",
            "description": "Explorando las fronteras de la realidad virtual",
            "avatar": "🔬"
        }
    ]
    
    # Datos de tecnología
    technologies = [
        {"name": "Three.js", "description": "Biblioteca 3D para WebGL"},
        {"name": "React", "description": "Framework de interfaz de usuario"},
        {"name": "Python", "description": "Backend y procesamiento de datos"},
        {"name": "WebGL", "description": "Gráficos 3D acelerados por hardware"},
        {"name": "Reflex", "description": "Framework web full-stack"},
        {"name": "Tailwind CSS", "description": "Framework de estilos utilitarios"}
    ]
    
    return html.div(
        # Encabezado
        Header.main(
            title="Acerca de Wold Virtual 3D",
            subtitle="Conoce más sobre nuestro proyecto y visión"
        ),
        
        # Navegación
        Navigation.main(
            items=nav_items,
            active_item="/about"
        ),
        
        # Contenido principal
        Container.main([
            # Sección de visión
            html.section(
                html.div(
                    html.div(
                        html.h2(
                            "Nuestra Visión",
                            class_name="text-3xl font-bold text-gray-900 mb-6"
                        ),
                        html.p(
                            "Wold Virtual 3D nace de la visión de crear espacios virtuales inmersivos que conecten a las personas de manera significativa. Creemos en el poder de la tecnología 3D para transformar la forma en que interactuamos, aprendemos y creamos en el mundo digital.",
                            class_name="text-lg text-gray-600 mb-8"
                        ),
                        html.p(
                            "Nuestro objetivo es democratizar el acceso a experiencias 3D de alta calidad, proporcionando herramientas intuitivas y plataformas accesibles para que cualquier persona pueda crear y explorar mundos virtuales.",
                            class_name="text-lg text-gray-600"
                        ),
                        class_name="max-w-4xl"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-white"
            ),
            
            # Sección de misión
            html.section(
                html.div(
                    html.div(
                        html.h2(
                            "Nuestra Misión",
                            class_name="text-3xl font-bold text-gray-900 mb-6"
                        ),
                        html.div(
                            [
                                html.div(
                                    html.div(
                                        html.div(
                                            str(i + 1),
                                            class_name="text-2xl font-bold text-blue-600"
                                        ),
                                        html.h3(
                                            mission["title"],
                                            class_name="text-xl font-semibold text-gray-900 mt-2"
                                        ),
                                        html.p(
                                            mission["description"],
                                            class_name="text-gray-600 mt-2"
                                        ),
                                        class_name="text-center"
                                    ),
                                    class_name="col-span-1"
                                ) for i, mission in enumerate([
                                    {
                                        "title": "Innovación Constante",
                                        "description": "Desarrollamos tecnologías de vanguardia para crear experiencias únicas"
                                    },
                                    {
                                        "title": "Accesibilidad Universal",
                                        "description": "Hacemos que las experiencias 3D estén disponibles para todos"
                                    },
                                    {
                                        "title": "Comunidad Global",
                                        "description": "Construimos una comunidad de creadores y exploradores virtuales"
                                    }
                                ])
                            ],
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-8"
                        ),
                        class_name="max-w-6xl"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-gray-50"
            ),
            
            # Sección de tecnología
            html.section(
                html.div(
                    html.h2(
                        "Tecnologías",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-12"
                    ),
                    html.div(
                        [
                            Card.basic(
                                title=tech["name"],
                                content=tech["description"]
                            ) for tech in technologies
                        ],
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-white"
            ),
            
            # Sección del equipo
            html.section(
                html.div(
                    html.h2(
                        "Nuestro Equipo",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-12"
                    ),
                    html.div(
                        [
                            Card.basic(
                                title=member["name"],
                                content=[
                                    html.div(
                                        member["avatar"],
                                        class_name="text-4xl mb-4"
                                    ),
                                    html.h4(
                                        member["role"],
                                        class_name="text-lg font-semibold text-blue-600 mb-2"
                                    ),
                                    html.p(
                                        member["description"],
                                        class_name="text-gray-600"
                                    )
                                ]
                            ) for member in team_members
                        ],
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-8"
                    ),
                    class_name="py-16"
                ),
                class_name="bg-gray-50"
            ),
            
            # Sección de contacto
            html.section(
                html.div(
                    html.div(
                        html.h2(
                            "¿Tienes preguntas?",
                            class_name="text-3xl font-bold text-white mb-4"
                        ),
                        html.p(
                            "Nos encantaría escuchar de ti. Contáctanos para más información sobre Wold Virtual 3D.",
                            class_name="text-xl text-blue-100 mb-8"
                        ),
                        html.div(
                            [
                                Button.primary("Contactar", href="/contact"),
                                Button.secondary("Documentación", href="/docs")
                            ],
                            class_name="flex space-x-4 justify-center"
                        ),
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