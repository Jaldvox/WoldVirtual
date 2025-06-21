# IA4pn.py - Evaluación del modelo

from sklearn.metrics import accuracy_score

def evaluar_modelo(modelo, data):
    # Dividir los datos en características y etiqueta
        X = data.drop("target", axis=1)
            y = data["target"]
                
                    # Realizar predicciones
                        predicciones = modelo.predict(X)
                            
                                # Calcular la precisión
                                    accuracy = accuracy_score(y, predicciones)
                                        
                                            print(f"Precisión del modelo: {accuracy * 100:.2f}%")
                                                return accuracy
