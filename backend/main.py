import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

sys.path.append(BASE_DIR)
from src.predict import calculate_hdi

# App Initialization
app = FastAPI(
    title="HDI Predictive Engine API",
    description="Asynchronous backend API driving the Energy and Economic HDI Calculator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Model
class HdiPredictionRequest(BaseModel):
    gdp_capita: float = Field(..., description="GDP per capita in USD", example=45000.0)
    elec_access: float = Field(..., description="Electricity access fraction [0.0 to 1.0]", example=1.0)
    consumption_capita: float = Field(..., description="Per capita electricity consumption in kWh", example=6500.0)
    outages: float = Field(..., description="Percentage of firms experiencing outages [0.0 to 1.0]", example=0.05)
    losses: float = Field(..., description="Transmission and distribution losses [0.0 to 1.0]", example=0.06)
    oil: float = Field(..., description="Oil share in electricity generation matrix [0.0 to 1.0]", example=0.20)
    gas: float = Field(..., description="Gas share in electricity generation matrix [0.0 to 1.0]", example=0.40)
    renewables: float = Field(..., description="Renewables share in electricity generation matrix [0.0 to 1.0]", example=0.40)

# API Routes
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.post("/predict")
async def predict_hdi(payload: HdiPredictionRequest):
    result = calculate_hdi(
        gdp_capita=payload.gdp_capita,
        elec_access=payload.elec_access,
        consumption_capita=payload.consumption_capita,
        outages=payload.outages,
        losses=payload.losses,
        oil=payload.oil,
        gas=payload.gas,
        renewables=payload.renewables
    )

    if isinstance(result, str) and "Error" in result:
        raise HTTPException(status_code=500, detail=result)

    return {
        "estimated_hdi": result,
        "interpretation": "Very High" if result >= 0.800 else "High" if result >= 0.700 else "Medium" if result >= 0.550 else "Low"
    }

# Static Files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")