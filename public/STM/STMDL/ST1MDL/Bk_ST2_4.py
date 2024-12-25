from BK_ST2_1_nodo import iniciar_servidor
from BK_ST2_1_sincronizacion import sincronizar_blockchain
from BK_ST2_1 import cargar_blockchain

def main():
    # Sincronizar la blockchain con otros nodos
    blockchain = sincronizar_blockchain()
    
    # Iniciar el servidor del nodo
    iniciar_servidor()

if __name__ == "__main__":
    main()
