"""
Componentes de UI básicos para Wold Virtual 3D
Componentes reutilizables para la interfaz de usuario
"""

from reflex import html, css
from typing import Optional, List, Dict, Any


class Button:
    """Componente de botón reutilizable"""
    
    @staticmethod
    def primary(
        text: str,
        on_click: Optional[str] = None,
        disabled: bool = False,
        size: str = "medium",
        **kwargs
    ):
        """Botón primario con estilos predefinidos"""
        size_classes = {
            "small": "px-3 py-1 text-sm",
            "medium": "px-4 py-2 text-base", 
            "large": "px-6 py-3 text-lg"
        }
        
        return html.button(
            text,
            class_name=f"bg-blue-600 hover:bg-blue-700 text-white font-bold rounded {size_classes.get(size, size_classes['medium'])} disabled:opacity-50 disabled:cursor-not-allowed",
            on_click=on_click,
            disabled=disabled,
            **kwargs
        )
    
    @staticmethod
    def secondary(
        text: str,
        on_click: Optional[str] = None,
        disabled: bool = False,
        size: str = "medium",
        **kwargs
    ):
        """Botón secundario con estilos predefinidos"""
        size_classes = {
            "small": "px-3 py-1 text-sm",
            "medium": "px-4 py-2 text-base",
            "large": "px-6 py-3 text-lg"
        }
        
        return html.button(
            text,
            class_name=f"bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded {size_classes.get(size, size_classes['medium'])} disabled:opacity-50 disabled:cursor-not-allowed",
            on_click=on_click,
            disabled=disabled,
            **kwargs
        )


class Card:
    """Componente de tarjeta para mostrar contenido"""
    
    @staticmethod
    def basic(
        title: Optional[str] = None,
        content: Any = None,
        footer: Optional[str] = None,
        **kwargs
    ):
        """Tarjeta básica con título, contenido y pie opcional"""
        return html.div(
            html.div(
                html.h3(title, class_name="text-lg font-semibold mb-2") if title else None,
                html.div(content, class_name="text-gray-700") if content else None,
                html.div(footer, class_name="text-sm text-gray-500 mt-4") if footer else None,
                class_name="p-6"
            ),
            class_name="bg-white rounded-lg shadow-md border border-gray-200",
            **kwargs
        )


class Container:
    """Contenedor principal para organizar contenido"""
    
    @staticmethod
    def main(
        children: List[Any],
        max_width: str = "max-w-7xl",
        padding: str = "px-4 py-8",
        **kwargs
    ):
        """Contenedor principal centrado"""
        return html.div(
            children,
            class_name=f"mx-auto {max_width} {padding}",
            **kwargs
        )
    
    @staticmethod
    def fluid(
        children: List[Any],
        padding: str = "px-4 py-8",
        **kwargs
    ):
        """Contenedor fluido que ocupa todo el ancho"""
        return html.div(
            children,
            class_name=f"w-full {padding}",
            **kwargs
        )


class Header:
    """Componente de encabezado de página"""
    
    @staticmethod
    def main(
        title: str,
        subtitle: Optional[str] = None,
        actions: Optional[List[Any]] = None,
        **kwargs
    ):
        """Encabezado principal con título, subtítulo y acciones"""
        return html.header(
            html.div(
                html.div(
                    html.h1(title, class_name="text-3xl font-bold text-gray-900"),
                    html.p(subtitle, class_name="text-lg text-gray-600 mt-2") if subtitle else None,
                    class_name="flex-1"
                ),
                html.div(
                    actions,
                    class_name="flex space-x-4"
                ) if actions else None,
                class_name="flex items-center justify-between"
            ),
            class_name="bg-white border-b border-gray-200 px-6 py-4",
            **kwargs
        )


class Footer:
    """Componente de pie de página"""
    
    @staticmethod
    def main(
        content: str = "© 2024 Wold Virtual 3D. Todos los derechos reservados.",
        links: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        """Pie de página con contenido y enlaces opcionales"""
        return html.footer(
            html.div(
                html.div(
                    html.p(content, class_name="text-gray-600"),
                    class_name="flex-1"
                ),
                html.nav(
                    html.ul(
                        [
                            html.li(
                                html.a(
                                    link["text"],
                                    href=link["url"],
                                    class_name="text-gray-600 hover:text-gray-900"
                                )
                            ) for link in links
                        ] if links else [],
                        class_name="flex space-x-6"
                    ),
                    class_name="flex-1 flex justify-end"
                ) if links else None,
                class_name="flex items-center justify-between"
            ),
            class_name="bg-gray-50 border-t border-gray-200 px-6 py-4",
            **kwargs
        )


class Navigation:
    """Componente de navegación"""
    
    @staticmethod
    def main(
        items: List[Dict[str, str]],
        active_item: Optional[str] = None,
        **kwargs
    ):
        """Navegación principal con elementos y estado activo"""
        return html.nav(
            html.ul(
                [
                    html.li(
                        html.a(
                            item["text"],
                            href=item["url"],
                            class_name=f"px-3 py-2 rounded-md text-sm font-medium {'bg-blue-100 text-blue-700' if active_item == item['url'] else 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'}"
                        )
                    ) for item in items
                ],
                class_name="flex space-x-4"
            ),
            class_name="bg-white border-b border-gray-200 px-6 py-4",
            **kwargs
        ) 