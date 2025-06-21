"""
Componentes de formularios para Wold Virtual 3D
Formularios reutilizables para la aplicación
"""

from reflex import html, input, label, textarea, select, option
from typing import Optional, List, Dict, Any, Callable


class LoginForm:
    """Componente de formulario de inicio de sesión"""
    
    @staticmethod
    def basic(
        on_submit: Optional[Callable] = None,
        username_placeholder: str = "Nombre de usuario",
        password_placeholder: str = "Contraseña",
        submit_text: str = "Iniciar Sesión",
        **kwargs
    ):
        """Formulario básico de inicio de sesión"""
        return html.form(
            html.div(
                html.div(
                    label("Usuario", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="text",
                        name="username",
                        placeholder=username_placeholder,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Contraseña", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="password",
                        name="password",
                        placeholder=password_placeholder,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-6"
                ),
                html.button(
                    submit_text,
                    type="submit",
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                ),
                class_name="space-y-4"
            ),
            on_submit=on_submit,
            class_name="bg-white p-8 rounded-lg shadow-md border border-gray-200",
            **kwargs
        )


class RegistrationForm:
    """Componente de formulario de registro"""
    
    @staticmethod
    def basic(
        on_submit: Optional[Callable] = None,
        submit_text: str = "Registrarse",
        **kwargs
    ):
        """Formulario básico de registro"""
        return html.form(
            html.div(
                html.div(
                    label("Nombre completo", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="text",
                        name="full_name",
                        placeholder="Tu nombre completo",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Email", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="email",
                        name="email",
                        placeholder="tu@email.com",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Usuario", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="text",
                        name="username",
                        placeholder="Nombre de usuario",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Contraseña", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="password",
                        name="password",
                        placeholder="Contraseña",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Confirmar contraseña", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="password",
                        name="confirm_password",
                        placeholder="Confirma tu contraseña",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-6"
                ),
                html.button(
                    submit_text,
                    type="submit",
                    class_name="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                ),
                class_name="space-y-4"
            ),
            on_submit=on_submit,
            class_name="bg-white p-8 rounded-lg shadow-md border border-gray-200",
            **kwargs
        )


class SettingsForm:
    """Componente de formulario de configuración"""
    
    @staticmethod
    def basic(
        on_submit: Optional[Callable] = None,
        submit_text: str = "Guardar Cambios",
        **kwargs
    ):
        """Formulario básico de configuración"""
        return html.form(
            html.div(
                html.div(
                    label("Nombre de usuario", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="text",
                        name="username",
                        placeholder="Tu nombre de usuario",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Email", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    input(
                        type="email",
                        name="email",
                        placeholder="tu@email.com",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Tema", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    select(
                        option("Claro", value="light"),
                        option("Oscuro", value="dark"),
                        option("Automático", value="auto"),
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-4"
                ),
                html.div(
                    label("Idioma", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    select(
                        option("Español", value="es"),
                        option("English", value="en"),
                        option("Français", value="fr"),
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-6"
                ),
                html.div(
                    label("Biografía", class_name="block text-sm font-medium text-gray-700 mb-1"),
                    textarea(
                        name="bio",
                        placeholder="Cuéntanos sobre ti...",
                        rows=4,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    class_name="mb-6"
                ),
                html.button(
                    submit_text,
                    type="submit",
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                ),
                class_name="space-y-4"
            ),
            on_submit=on_submit,
            class_name="bg-white p-8 rounded-lg shadow-md border border-gray-200",
            **kwargs
        ) 