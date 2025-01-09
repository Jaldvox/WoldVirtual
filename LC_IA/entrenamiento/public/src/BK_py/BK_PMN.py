"""
This script demonstrates the usage of Reflex and Blockchain modules.
"""

from modules.reflex import Reflex
from modules.blockchain import Blockchain

def main():
    """
    Main function to demonstrate the usage of Reflex and Blockchain modules.
    """
    reflex = Reflex()
    blockchain = Blockchain()

    # Ejemplo de uso de Reflex
    reflex.run()

    # Ejemplo de uso de Blockchain
    blockchain.add_block("Primer bloque de datos")
    blockchain.print_chain()

if __name__ == "__main__":
    main()
