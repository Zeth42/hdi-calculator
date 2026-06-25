import os
import numpy as np
import joblib

# Load the trained model into memory globally
MODEL_PATH = os.path.join('models', 'hdi_model.pkl')
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

def calculate_hdi(gdp_capita, elec_access, consumption_capita, outages, losses, oil, gas, renewables):
    if model is None:
        return "Error: Model artifact not found. Please train the model first."
    
    # Apply the same log transformation used during training
    gdp_log = np.log1p(gdp_capita)
    
    # Structure the inputs to match the training feature order
    input_data = np.array([[
        gdp_log, elec_access, consumption_capita, 
        outages, losses, oil, gas, renewables
    ]])
    
    # Predict and bound the output within logical HDI limits [0, 1]
    prediction = model.predict(input_data)[0]
    final_hdi = max(0.0, min(1.0, prediction))
    
    return round(final_hdi, 3)

# Quick sanity check / smoke test
if __name__ == '__main__':
    print("--- Testing HDI Calculator Engine ---")
    # Sample prediction using proxy values for a high-income profile
    sample_result = calculate_hdi(
        gdp_capita=45000, elec_access=1.0, consumption_capita=6000, 
        outages=0.05, losses=0.06, oil=0.2, gas=0.4, renewables=0.4
    )
    print(f"Estimated HDI for sample input: {sample_result}")