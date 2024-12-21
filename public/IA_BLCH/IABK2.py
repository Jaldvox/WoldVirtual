from sklearn.ensemble import RandomForestClassifier
import pickle

class SimpleAI:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.X_train = []
        self.y_train = []

    def train(self, X, y):
        self.X_train.extend(X)
        self.y_train.extend(y)
        self.model.fit(self.X_train, self.y_train)

    def predict(self, data):
        return self.model.predict(data)

    def save_model(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, file_path):
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
