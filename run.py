#!/usr/bin/env python3
"""
Google Search Trends Project - Auto Setup and Run Script

This script automatically:
1. Checks and installs Python dependencies
2. Checks and installs Node.js dependencies
3. Sets up environment files
4. Starts both the Python backend and Next.js frontend
5. Opens the application in your browser

Usage: python run.py
"""

import os
import sys
import subprocess
import platform
import time
import webbrowser
from pathlib import Path
import json

class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_status(message, color=Colors.OKBLUE):
    """Print a status message with color."""
    print(f"{color}{message}{Colors.ENDC}")

def print_success(message):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message."""
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8+ is required. Current version: {}.{}".format(version.major, version.minor))
        return False
    print_success(f"Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed and version is compatible."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True, shell=True)
        version = result.stdout.strip()
        print_success(f"Node.js version {version} is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is available."""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, check=True, shell=True)
        version = result.stdout.strip()
        print_success(f"npm version {version} is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("npm is not available. Please install Node.js with npm.")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    print_status("Installing Python dependencies...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path(".venv")
    if not venv_path.exists():
        print_status("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print_success("Virtual environment created")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to create virtual environment: {e}")
            return False
    
    # Determine the pip command for the virtual environment
    if platform.system() == "Windows":
        pip_cmd = ".venv\\Scripts\\pip"
        python_cmd = ".venv\\Scripts\\python"
    else:
        pip_cmd = ".venv/bin/pip"
        python_cmd = ".venv/bin/python"
    
    # Upgrade pip
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        print_success("pip upgraded")
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to upgrade pip: {e}")
    
    # Install dependencies
    try:
        # Install core dependencies first
        core_deps = [
            "requests", "pandas", "numpy", "matplotlib", "seaborn", "plotly",
            "fastapi", "uvicorn", "python-dotenv", "pydantic", "pytrends"
        ]
        
        for dep in core_deps:
            try:
                subprocess.run([pip_cmd, "install", dep], check=True)
                print_success(f"Installed {dep}")
            except subprocess.CalledProcessError:
                print_warning(f"Failed to install {dep}, trying with --user flag")
                subprocess.run([pip_cmd, "install", "--user", dep], check=True)
        
        # Try to install from requirements.txt if it exists
        if Path("requirements.txt").exists():
            try:
                subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
                print_success("Installed dependencies from requirements.txt")
            except subprocess.CalledProcessError as e:
                print_warning(f"Some dependencies from requirements.txt failed to install: {e}")
        
        return True
    except Exception as e:
        print_error(f"Failed to install Python dependencies: {e}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies."""
    print_status("Installing Node.js dependencies...")
    
    webapp_path = Path("webapp")
    if not webapp_path.exists():
        print_error("webapp directory not found")
        return False
    
    try:
        # Change to webapp directory
        os.chdir(webapp_path)
        
        # Install dependencies
        subprocess.run(["npm", "install"], check=True)
        print_success("Node.js dependencies installed")
        
        # Change back to root directory
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install Node.js dependencies: {e}")
        os.chdir("..")  # Make sure we're back in the root directory
        return False

def setup_environment_files():
    """Set up environment files if they don't exist."""
    print_status("Setting up environment files...")
    
    # Copy env.example to .env if it doesn't exist
    if Path("env.example").exists() and not Path(".env").exists():
        try:
            with open("env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print_success("Created .env file from env.example")
        except Exception as e:
            print_warning(f"Failed to create .env file: {e}")
    
    # Copy webapp env.example to .env.local if it doesn't exist
    webapp_env_example = Path("webapp/env.example")
    webapp_env_local = Path("webapp/.env.local")
    
    if webapp_env_example.exists() and not webapp_env_local.exists():
        try:
            with open(webapp_env_example, "r") as src, open(webapp_env_local, "w") as dst:
                dst.write(src.read())
            print_success("Created webapp/.env.local file")
        except Exception as e:
            print_warning(f"Failed to create webapp/.env.local file: {e}")

def create_directories():
    """Create necessary directories."""
    print_status("Creating necessary directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/exports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success("Directories created")

def start_services():
    """Start the Python backend and Next.js frontend."""
    print_status("Starting services...")
    
    # Start Next.js frontend in background
    print_status("Starting Next.js frontend...")
    try:
        os.chdir("webapp")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        os.chdir("..")
        print_success("Next.js frontend started")
        
        # Wait a bit for frontend to start
        time.sleep(5)
        
        # Start Python backend
        print_status("Starting Python backend...")
        backend_process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_success("Python backend started")
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Open browser
        print_status("Opening application in browser...")
        try:
            webbrowser.open("http://localhost:3000")
            print_success("Application opened in browser")
        except Exception as e:
            print_warning(f"Failed to open browser automatically: {e}")
            print_status("Please open http://localhost:3000 in your browser")
        
        print_success("🎉 Application is running!")
        print_status("Frontend: http://localhost:3000")
        print_status("Backend API: http://localhost:8000")
        print_status("API Docs: http://localhost:8000/docs")
        
        print_warning("Press Ctrl+C to stop the services")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_status("Stopping services...")
            frontend_process.terminate()
            backend_process.terminate()
            print_success("Services stopped")
            
    except Exception as e:
        print_error(f"Failed to start services: {e}")
        return False

def main():
    """Main function to run the setup and start the application."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("🚀 Google Search Trends Project - Auto Setup & Run")
    print("=" * 60)
    print(f"{Colors.ENDC}")
    
    # Check prerequisites
    print_status("Checking prerequisites...")
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    if not check_npm():
        return False
    
    # Install dependencies
    if not install_python_dependencies():
        return False
    
    if not install_node_dependencies():
        return False
    
    # Setup environment
    setup_environment_files()
    create_directories()
    
    # Start services
    start_services()

if __name__ == "__main__":
    main() 