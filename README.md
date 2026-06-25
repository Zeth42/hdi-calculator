# HDI Calculator (Predictive Model Based on Energy and Economic Metrics)

This project develops a multivariate predictive model designed to estimate a country's Human Development Index (HDI) by analyzing the interplay between its electrical infrastructure, energy matrix, and economic capacity (GDP per Capita).

Inspired by multivariate probabilistic modeling and predictive analytics workflows for data-driven research.

## Data Source & Features
The model trains on a consolidated global dataset (2023 metrics) utilizing the following features:
* **Economic:** GDP per Capita (USD) and Population.
* **Grid Quality & Infrastructure:** % Electricity Access, Per Capita Consumption (kWh), Percentage of firms experiencing outages, and Transmission losses.
* **Energy Matrix:** Percentage share of Oil, Gas, and Renewables in electricity generation.

## System Architecture
The repository follows a clean, modular structure split into three primary layers:
1. **Machine Learning Core (`src/`):** Python scripts that handle data loading, apply log transformations to stabilize skewed GDP metrics, fit regression algorithms, and export the trained model artifact (`.pkl`).
2. **Backend API (`backend/`):** A lightweight asynchronous REST API built with **FastAPI** that loads the model into memory and exposes a prediction endpoint.
3. **Frontend Client (`frontend/`):** An interactive web UI that consumes the API, allowing users to simulate development scenarios using input sliders.

## Installation & Setup

### Environment Configuration
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/hdi-calculator.git](https://github.com/YOUR_USERNAME/hdi-calculator.git)
   cd hdi-calculator