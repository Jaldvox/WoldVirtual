import os
from .IABK1 import Blockchain,
from .IABK2 import SimpleAI,

class System:
    def __init__(self):
        self.blockchain = Blockchain()
        self.ai = SimpleAI()
        self.good_results = []
        self.bad_results = []

    def train_ai(self):
        if self.good_results:
            X, y = zip(*self.good_results)
            self.ai.train(X, y)
        self.ai.save_model('ai_model.pkl')

    def handle_bad_results(self):
        if self.bad_results:
            # Aquí puedes definir cómo reajustar los datos malos para corregir errores
            # Por ejemplo, podrías ajustar hiperparámetros, realizar validaciones adicionales, etc.
            pass

    def add_transaction(self, sender, recipient, amount):
        index = self.blockchain.new_transaction(sender, recipient, amount)
        return index

    def mine_block(self):
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)
        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.new_block(proof, previous_hash)
        return block

    def label_result(self, data, label, is_good):
        if is_good:
            self.good_results.append((data, label))
        else:
            self.bad_results.append((data, label))
        self.train_ai()
        self.handle_bad_results()

    def run(self):
        if not os.path.exists('ai_model.pkl'):
            self.train_ai()
        self.ai.load_model('ai_model.pkl')

        # Ejemplo de uso
        print("Adding transaction...")
        self.add_transaction("Alice", "Bob", 100)

        print("Mining block...")
        block = self.mine_block()
        print(f"New Block: {block}")

        # Ejemplo de etiquetado de resultados
        sample_data = [[5.1, 3.5, 1.4, 0.2]]  # Ejemplo de datos de entrada
        prediction = self.ai.predict(sample_data)
        print(f"Prediction: {prediction}")

        # Etiquetar el resultado como bueno o malo
        self.label_result(sample_data, prediction, is_good=True)  # Cambiar is_good=True/False según corresponda

if __name__ == "__main__":
    system = System()
    system.run()
