# IA3pn.py - Entrenamiento del modelo

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def entrenar_modelo(data):
    # Dividir en características y etiqueta
        X = data.drop("target", axis=1)
            y = data["target"]
                
                    # Dividir los datos en entrenamiento y prueba
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                            
                                # Crear y entrenar el modelo
                                    modelo = LogisticRegression()
                                        modelo.fit(X_train, y_train)
                                            
                                                return modelo
                                                