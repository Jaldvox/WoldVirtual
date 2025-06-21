"""
Componentes de datos para Wold Virtual 3D
Componentes para mostrar y manejar datos
"""

from reflex import html, table, tr, td, th, thead, tbody
from typing import Optional, List, Dict, Any


class DataTable:
    """Componente de tabla de datos"""
    
    @staticmethod
    def basic(
        headers: List[str],
        data: List[List[Any]],
        striped: bool = True,
        hover: bool = True,
        **kwargs
    ):
        """Tabla básica con encabezados y datos"""
        table_classes = "min-w-full divide-y divide-gray-200"
        if striped:
            table_classes += " bg-white"
        
        return html.div(
            table(
                thead(
                    tr(
                        [th(header, class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider") for header in headers],
                        class_name="bg-gray-50"
                    )
                ),
                tbody(
                    [
                        tr(
                            [td(cell, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900") for cell in row],
                            class_name=f"{'bg-gray-50' if striped and i % 2 == 1 else 'bg-white'} {'hover:bg-gray-100' if hover else ''}"
                        ) for i, row in enumerate(data)
                    ],
                    class_name="bg-white divide-y divide-gray-200"
                ),
                class_name=table_classes
            ),
            class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
            **kwargs
        )
    
    @staticmethod
    def with_actions(
        headers: List[str],
        data: List[List[Any]],
        actions: List[Dict[str, Any]],
        **kwargs
    ):
        """Tabla con acciones por fila"""
        # Agregar columna de acciones al final
        full_headers = headers + ["Acciones"]
        
        def create_action_buttons(row_index: int):
            return html.div(
                [
                    html.button(
                        action["text"],
                        class_name=f"text-{action.get('color', 'blue')}-600 hover:text-{action.get('color', 'blue')}-900 mr-2",
                        on_click=action.get("on_click", lambda: None)
                    ) for action in actions
                ],
                class_name="flex space-x-2"
            )
        
        full_data = [row + [create_action_buttons(i)] for i, row in enumerate(data)]
        
        return DataTable.basic(full_headers, full_data, **kwargs)


class Chart:
    """Componente de gráficos"""
    
    @staticmethod
    def line(
        data: List[Dict[str, Any]],
        title: Optional[str] = None,
        width: str = "100%",
        height: str = "400px",
        **kwargs
    ):
        """Gráfico de líneas"""
        return html.div(
            html.canvas(
                id="line-chart",
                class_name="w-full h-full"
            ),
            script(src="/static/js/chart.js"),
            script(f"""
                const ctx = document.getElementById('line-chart').getContext('2d');
                new Chart(ctx, {{
                    type: 'line',
                    data: {data},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: {str(title is not None).lower()},
                                text: '{title or ""}'
                            }}
                        }}
                    }}
                }});
            """),
            style={"width": width, "height": height},
            class_name="bg-white p-4 rounded-lg shadow-md border border-gray-200",
            **kwargs
        )
    
    @staticmethod
    def bar(
        data: List[Dict[str, Any]],
        title: Optional[str] = None,
        width: str = "100%",
        height: str = "400px",
        **kwargs
    ):
        """Gráfico de barras"""
        return html.div(
            html.canvas(
                id="bar-chart",
                class_name="w-full h-full"
            ),
            script(src="/static/js/chart.js"),
            script(f"""
                const ctx = document.getElementById('bar-chart').getContext('2d');
                new Chart(ctx, {{
                    type: 'bar',
                    data: {data},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: {str(title is not None).lower()},
                                text: '{title or ""}'
                            }}
                        }}
                    }}
                }});
            """),
            style={"width": width, "height": height},
            class_name="bg-white p-4 rounded-lg shadow-md border border-gray-200",
            **kwargs
        )
    
    @staticmethod
    def pie(
        data: List[Dict[str, Any]],
        title: Optional[str] = None,
        width: str = "100%",
        height: str = "400px",
        **kwargs
    ):
        """Gráfico circular"""
        return html.div(
            html.canvas(
                id="pie-chart",
                class_name="w-full h-full"
            ),
            script(src="/static/js/chart.js"),
            script(f"""
                const ctx = document.getElementById('pie-chart').getContext('2d');
                new Chart(ctx, {{
                    type: 'pie',
                    data: {data},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: {str(title is not None).lower()},
                                text: '{title or ""}'
                            }}
                        }}
                    }}
                }});
            """),
            style={"width": width, "height": height},
            class_name="bg-white p-4 rounded-lg shadow-md border border-gray-200",
            **kwargs
        )


class StatusIndicator:
    """Componente de indicador de estado"""
    
    @staticmethod
    def basic(
        status: str,
        text: Optional[str] = None,
        size: str = "medium",
        **kwargs
    ):
        """Indicador de estado básico"""
        status_colors = {
            "success": "bg-green-500",
            "error": "bg-red-500",
            "warning": "bg-yellow-500",
            "info": "bg-blue-500",
            "pending": "bg-gray-500"
        }
        
        size_classes = {
            "small": "w-2 h-2",
            "medium": "w-3 h-3",
            "large": "w-4 h-4"
        }
        
        return html.div(
            html.div(
                html.div(
                    class_name=f"{status_colors.get(status, 'bg-gray-500')} {size_classes.get(size, size_classes['medium'])} rounded-full"
                ),
                html.span(
                    text or status.title(),
                    class_name="ml-2 text-sm font-medium text-gray-900"
                ) if text or status else None,
                class_name="flex items-center"
            ),
            class_name="inline-flex items-center",
            **kwargs
        )
    
    @staticmethod
    def with_icon(
        status: str,
        icon: str,
        text: str,
        **kwargs
    ):
        """Indicador de estado con icono"""
        status_styles = {
            "success": "text-green-600 bg-green-100",
            "error": "text-red-600 bg-red-100",
            "warning": "text-yellow-600 bg-yellow-100",
            "info": "text-blue-600 bg-blue-100",
            "pending": "text-gray-600 bg-gray-100"
        }
        
        return html.div(
            html.div(
                html.span(
                    icon,
                    class_name="text-lg"
                ),
                html.span(
                    text,
                    class_name="ml-2 text-sm font-medium"
                ),
                class_name="flex items-center"
            ),
            class_name=f"inline-flex items-center px-3 py-1 rounded-full text-sm font-medium {status_styles.get(status, status_styles['pending'])}",
            **kwargs
        ) 