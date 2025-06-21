"""
This module contains several applications that manage different aspects of the system.
"""

from reflex import ReflexApp

class BK_App(ReflexApp):
    """
    BK_App class that provides an overview of the module.
    """
    def __init__(self):
        """
        Initialize the BK_App class.
        """
        super().__init__()
        self.title = "BK_App Overview"
        self.description = """
        Este módulo contiene varias aplicaciones que gestionan diferentes aspectos del sistema:
        - BK_1App: Módulo principal con el menú de secciones.
        - BK_2App: Gestión de usuarios.
        - BK_3App: Gestión de recursos.
        - BK_4App: Gestión de blockchain.
        - BK_5App: Gestión de compresión de datos.
        """

    def render(self):
        """
        Render the BK_App overview.
        """
        return f"""
        <h1>{self.title}</h1>
        <p>{self.description}</p>
        """

if __name__ == "__main__":
    app = BK_App()
    app.run()
