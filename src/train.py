import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def train_model():
    # 1. Cargar datos (ajusta la ruta y saltar filas si es necesario)
    data_path = os.path.join('data', 'IDH_Consolidado_PIB_y_Energia_2023-v7.csv')
    df = pd.read_csv(data_path, skiprows=3)
    
    # 2. Transformación logarítmica del PIB para estabilizar varianzas
    df['PIB_Log'] = np.log1p(df['PIB per Cápita (USD)'])
    
    # 3. Definir características (X) y objetivo (y)
    features = [
        'PIB_Log', '% Acceso a Electricidad', 'Consumo per Cápita (kWh)',
        'Empresas con Apagones (%)', 'Pérdidas por Transmisión (%)',
        '% Petróleo', '% Gas', '% Renovables'
    ]
    
    X = df[features]
    y = df['IDH (2023)']
    
    # 4. Dividir en set de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Entrenar el modelo (Regresión Lineal para empezar)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluar rápidamente en consola
    score = model.score(X_test, y_test)
    print(f"Modelo entrenado exitosamente. R² en test: {score:.4f}")
    
    # 6. Guardar el modelo en la carpeta correspondiente
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'idh_model.pkl')
    joblib.dump(model, model_path)
    print(f"Modelo guardado en: {model_path}")

if __name__ == '__main__':
    train_model()