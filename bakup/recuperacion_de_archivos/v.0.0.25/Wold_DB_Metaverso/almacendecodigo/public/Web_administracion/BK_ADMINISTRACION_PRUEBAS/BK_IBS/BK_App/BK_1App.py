"""
This script serves as the main application with a menu of sections.
"""

from reflex import ReflexApp
from Web_administracion.BK_ADMINISTRACION_PRUEBAS.BK_IBS.BK_App.BK_2App import BK_2App
from Web_administracion.BK_ADMINISTRACION_PRUEBAS.BK_IBS.BK_App.BK_3App import BK_3App
from Web_administracion.BK_ADMINISTRACION_PRUEBAS.BK_IBS.BK_App.BK_4App import BK_4App
from Web_administracion.BK_ADMINISTRACION_PRUEBAS.BK_IBS.BK_App.BK_5App import BK_5App

class MainApp(ReflexApp):
    """
    MainApp class that initializes the main menu with sections.
    """
    def __init__(self):
        """
        Initialize the MainApp class.
        """
        super().__init__()
        self.title = "Main Menu"
        self.sections = {
            "Usuarios": BK_2App(),
            "Recursos": BK_3App(),
            "Blockchain": BK_4App(),
            "Compresión": BK_5App()
        }

    def render(self):
        """
        Render the main menu with the sections.
        """
        return self.menu(self.sections)

if __name__ == "__main__":
    app = MainApp()
    app.run()
