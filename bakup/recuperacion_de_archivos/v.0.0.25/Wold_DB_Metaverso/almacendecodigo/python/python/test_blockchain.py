from __init__ import Blockchain, print_block_info, BlockchainError

def main():
    try:
        # Crear nueva blockchain
        blockchain = Blockchain()
        print("Blockchain iniciada con bloque génesis")
        print_block_info(blockchain.chain[0])

        # Añadir algunos bloques
        block1 = blockchain.add_block("Datos del Bloque 1")
        print("\nBloque 1 añadido")
        print_block_info(block1)

        block2 = blockchain.add_block("Datos del Bloque 2")
        print("\nBloque 2 añadido")
        print_block_info(block2)

        # Verificar la cadena
        is_valid = blockchain.verify_chain()
        print(f"\nLa blockchain es válida: {is_valid}")
        
        # Mostrar toda la cadena
        print("\n=== Cadena Completa ===")
        for block in blockchain.chain:
            print_block_info(block)

    except BlockchainError as e:
        print(f"Error en la blockchain: {e.mensaje}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()