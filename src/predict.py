import os
import numpy as np
import joblib

# Cargar el modelo de manera global para que esté listo en memoria
MODEL_PATH = os.path.join('models', 'idh_model.pkl')
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

def calcular_idh(pib_capita, acceso_elec, consumo_capita, apagones, perdidas, petroleo, gas, renovables):
    if model is None:
        return "Error: El modelo no ha sido entrenado o no se encuentra en la ruta."
    
    # Aplicar la misma transformación que en el entrenamiento
    pib_log = np.log1p(pib_capita)
    
    # Estructurar los datos de entrada en el orden exacto de las features del modelo
    input_data = np.array([[
        pib_log, acceso_elec, consumo_capita, 
        apagones, perdidas, petroleo, gas, renovables
    ]])
    
    # Predecir y asegurar que no se salga de los límites lógicos del IDH [0, 1]
    prediccion = model.predict(input_data)[0]
    idh_final = max(0.0, min(1.0, prediccion))
    
    return round(idh_final, 3)

# Pequeña prueba de escritorio para verificar que funcione en consola
if __name__ == '__main__':
    print("--- Probando Calculadora de IDH ---")
    # Ejemplo con datos aproximados de un país de ingresos altos
    resultado = calcular_idh(
        pib_capita=45000, acceso_elec=1.0, consumo_capita=6000, 
        apagones=0.05, perdidas=0.06, petroleo=0.2, gas=0.4, renovables=0.4
    )
    print(f"IDH Estimado para el ejemplo: {resultado}")