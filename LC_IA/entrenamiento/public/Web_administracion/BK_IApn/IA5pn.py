# IA5pn.py - Realización de predicciones

def realizar_predicciones(modelo, data):
    # Dividir los datos en características
        X = data.drop("target", axis=1)
            
                # Realizar las predicciones
                    predicciones = modelo.predict(X)
                        
                            return predicciones
