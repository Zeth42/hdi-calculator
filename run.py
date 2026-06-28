import os
import sys
import subprocess
import webbrowser
import time

def run_project():
    print("Starting HDI Calculator Project Automation...")
    
    # 1. Get the absolute path of the project root
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Check if the trained model artifact exists
    model_path = os.path.join(root_dir, 'models', 'hdi_model.pkl')
    if not os.path.exists(model_path):
        print("Model artifact not found! Training the model first...")
        train_script = os.path.join(root_dir, 'src', 'train.py')
        subprocess.run([sys.executable, train_script], check=True)
        print("Model successfully trained.")
    
    # 3. Path to the frontend index.html file
    frontend_path = os.path.join(root_dir, 'frontend', 'index.html')
    
    # 4. Launch the FastAPI Backend Server as a background process
    print("Launching FastAPI backend server via Uvicorn...")
    
    # Using sys.executable guarantees it hooks to your specific Windows Store python version
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=root_dir
    )
    
    # 5. Grace period for the local port to open, then launch the interactive UI
    time.sleep(2.5)
    if os.path.exists(frontend_path):
        print(f"Opening user interface: {frontend_path}")
        webbrowser.open(f"file:///{frontend_path}")
    else:
        print("Warning: frontend/index.html not found yet. Open browser to http://127.0.0.1:8000/docs instead.")
        webbrowser.open("http://127.0.0.1:8000/docs")
        
    print("\nSystem is fully operational. Press CTRL+C in this terminal to shutdown the backend server.")
    
    try:
        # Keep the main process alive so the backend doesn't close immediately
        backend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down backend server safely...")
        backend_process.terminate()
        print("Project closed successfully.")

if __name__ == "__main__":
    run_project()