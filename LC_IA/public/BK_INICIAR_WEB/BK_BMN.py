"""
This script handles the initialization of the system, including blockchain creation and AI model training.
"""

import hashlib
import datetime
from BK_FN2 import process_transaction, validate_user, generate_report, update_database, send_notification
from BK_FN3 import log_activity, send_alert, backup_data, clear_cache, sync_data

# Clase Block para manejar los bloques
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_data.encode()).hexdigest()

# Clase SimpleBlockchain para manejar la cadena de bloques
class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, str(datetime.datetime.now()), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def create_block_from_BK_FN2(self):
        # Ejecutar funciones del módulo 1 (BK_FN2)
        function_results = []
        function_results.append(process_transaction())
        function_results.append(validate_user())
        function_results.append(generate_report())
        function_results.append(update_database())
        function_results.append(send_notification())

        # Crear y añadir un nuevo bloque con los resultados de las funciones
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.datetime.now()), function_results, previous_block.hash)
        self.chain.append(new_block)
        print("Nuevo bloque creado desde módulo BK_FN2 con funciones ejecutadas")

    def create_block_from_BK_FN3(self):
        # Ejecutar funciones del módulo 2 (BK_FN3)
        function_results = []
        function_results.append(log_activity())
        function_results.append(send_alert())
        function_results.append(backup_data())
        function_results.append(clear_cache())
        function_results.append(sync_data())

        # Crear y añadir un nuevo bloque con los resultados de las funciones
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.datetime.now()), function_results, previous_block.hash)
        self.chain.append(new_block)
        print("Nuevo bloque creado desde módulo BK_FN3 con funciones ejecutadas")

    def show_chain(self):
        for block in self.chain:
            print(f"Índice: {block.index}, Data: {block.data}, Hash: {block.hash}")

# Función principal que orquesta todo el sistema
def main():
    """
    Main function that orchestrates the entire system.
    It creates the blockchain, processes transactions, and trains the AI model.
    """
    # Paso 1: Crear la cadena de bloques
    blockchain = SimpleBlockchain()

    # Paso 2: Ejecutar funciones del sistema de IA (preparar datos, entrenar, evaluar, etc.)
    print("Preparando los datos...")
    data = preprocesar_datos("dataset.csv")  # Llamada al módulo de IA

    print("Entrenando el modelo...")
    modelo = entrenar_modelo(data)  # Llamada al módulo de entrenamiento de IA

    # Paso 3: Ejecutar funciones del sistema de blockchain y de IA
    print("Ejecutando funciones del sistema de blockchain...")
    blockchain.create_block_from_BK_FN2()  # Llamada al bloque 1
    blockchain.create_block_from_BK_FN3()  # Llamada al bloque 2

    # Mostrar la cadena de bloques
    blockchain.show_chain()

# Ejecutar el flujo principal
if __name__ == "__main__":
    main()
    
