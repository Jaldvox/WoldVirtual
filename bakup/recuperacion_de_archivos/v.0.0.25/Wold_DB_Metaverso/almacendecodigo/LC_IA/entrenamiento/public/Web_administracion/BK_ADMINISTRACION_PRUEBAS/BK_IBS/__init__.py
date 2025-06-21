"""
This script initializes the MainPlatform class and sets up the application modules.
"""

from freflex import ReflexApp
import sys
import os

# Añadir la ruta de la carpeta 'BK_Blockchain' al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BK_Blockchain')))

from BK_Blockchain import BK_Blockchain, Blockchain, GenesisBlock, AddBlock, ChainInfo, ValidateChain

class MainPlatform(ReflexApp):
    """
    MainPlatform class that initializes the application and sets up the modules.
    """
    def __init__(self):
        """
        Initialize the MainPlatform class.
        """
        super().__init__()
        self.title = "Main Platform"
        self.modules = {
            "Overview": BK_Blockchain(),
            "Blockchain": Blockchain(),
            "Genesis Block": GenesisBlock(),
            "Add Block": AddBlock(),
            "Chain Info": ChainInfo(),
            "Validate Chain": ValidateChain()
        }

    def render(self):
        """
        Render the main platform with the menu and content sections.
        """
        menu = "<ul>"
        for name, module in self.modules.items():
            menu += f"<li><a href='#{name}'>{name}</a></li>"
        menu += "</ul>"

        content = "<div>"
        for name, module in self.modules.items():
            content += f"<section id='{name}'>{module.render()}</section>"
        content += "</div>"

        return f"""
        <h1>{self.title}</h1>
        {menu}
        {content}
        """

if __name__ == "__main__":
    app = MainPlatform()
    app.run()
