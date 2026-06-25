import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def clean_numeric_value(val):
    if pd.isna(val): 
        return np.nan
    
    # Convert to string, strip spaces, and remove currency formatting symbols
    val_str = str(val).strip().replace(' ', '').replace('$', '').replace(',', '')
    
    # If it is a percentage string, strip the symbol and convert to a fraction [0, 1]
    if '%' in val_str:
        return float(val_str.replace('%', '')) / 100.0
        
    try:
        return float(val_str)
    except ValueError:
        return np.nan

def train_model():
    # 1. Load data dealing with Latin character encodings safely
    data_path = os.path.join('data', 'IDH_Consolidado_PIB_y_Energia_2023-v7.csv')
    df = pd.read_csv(data_path, skiprows=3, encoding='latin-1')
    
    # 2. Hardcode clean ASCII column headers to bypass encoding corruption
    df.columns = [
        'Country', 'HDI', 'GDP_per_Capita', 'Population', 'Electricity_Access',
        'Consumption_per_Capita', 'Outages', 'Transmission_Losses', 'Oil', 'Gas', 'Renewables'
    ]
    
    # 3. Map the cleaning function across all numerical columns
    numeric_cols = [
        'HDI', 'GDP_per_Capita', 'Population', 'Electricity_Access',
        'Consumption_per_Capita', 'Outages', 'Transmission_Losses', 'Oil', 'Gas', 'Renewables'
    ]
    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric_value)
    
    # 4. Drop rows with critical missing metrics
    df = df.dropna(subset=['HDI', 'GDP_per_Capita'])
    
    # 5. Apply log transformation to GDP per Capita to normalize distribution
    df['GDP_Log'] = np.log1p(df['GDP_per_Capita'])
    
    # 6. Define features (X) and target label (y)
    features = [
        'GDP_Log', 'Electricity_Access', 'Consumption_per_Capita', 
        'Outages', 'Transmission_Losses', 'Oil', 'Gas', 'Renewables'
    ]
    
    X = df[features]
    y = df['HDI']
    
    # 7. Split dataset into training and testing sets (80% training, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 8. Initialize and fit Multiple Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 9. Evaluate model performance using R² score
    score = model.score(X_test, y_test)
    print(f"Model successfully trained. R² score on test set: {score:.4f}")
    
    # 10. Export the trained model artifact to disk
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'hdi_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

if __name__ == '__main__':
    train_model()