FROM python:3.11-slim

WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application
COPY . .

# Train the model during build to ensure the pkl exists
RUN python src/train.py
RUN python -c "import os; p='/code/frontend'; print('frontend exists:', os.path.exists(p)); print('app.js exists:', os.path.exists(p+'/app.js'))"

# Run Uvicorn directly, serving backend on port 7860 (Hugging Face standard)
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]