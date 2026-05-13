#!/usr/bin/env python3
"""
EquityAI Environment Setup Script
Automates the setup process for the EquityAI Research Tool
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    if not venv_path.exists():
        return run_command("python -m venv venv", "Creating virtual environment")
    else:
        print("✅ Virtual environment already exists")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Use python -m pip for better compatibility
    commands = [
        "python -m pip install --upgrade pip",
        "python -m pip install -r requirements.txt"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            return False
    
    return True

def download_nlp_models():
    """Download required NLP models"""
    print("🧠 Downloading NLP models...")
    
    commands = [
        "python -m spacy download en_core_web_sm",
        "python -m pip install pydantic-settings",  # For config loading
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            print(f"⚠️  Warning: Failed to run {cmd}")
    
    return True

def setup_environment_file():
    """Create .env file from template"""
    print("⚙️  Setting up environment configuration...")
    
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists(".env.example"):
        print("❌ .env.example file not found")
        return False
    
    # Copy template
    with open(".env.example", "r") as f:
        content = f.read()
    
    with open(".env", "w") as f:
        f.write(content)
    
    print("✅ .env file created from template")
    print("📝 Please edit .env file with your API keys and configuration")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "logs",
        "data",
        "models",
        "static",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")
    
    return True

def test_installation():
    """Test installation"""
    print("🧪 Testing installation...")
    
    # Test imports
    test_script = """
import sys
sys.path.append('backend')

try:
    from app.nlp.sentiment_analyzer import SentimentAnalyzer
    from app.nlp.entity_extractor import EntityExtractor
    from app.nlp.text_summarizer import TextSummarizer
    print("✅ All NLP modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

try:
    import streamlit
    import plotly
    import pandas
    import requests
    print("✅ All frontend dependencies imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

print("🎉 Installation test passed!")
"""
    
    with open("test_install.py", "w") as f:
        f.write(test_script)
    
    success = run_command("python test_install.py", "Running installation test")
    
    # Clean up test file
    Path("test_install.py").unlink(missing_ok=True)
    
    return success

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("\n1. 📝 Edit your .env file:")
    print("   - Add your NewsAPI key (optional)")
    print("   - Add your OpenAI API key (optional)")
    print("   - Configure database settings")
    
    print("\n2. 🚀 Start the application:")
    print("   Backend:  cd backend && python run.py")
    print("   Frontend: cd frontend && streamlit run app.py")
    
    print("\n3. 🌐 Access the application:")
    print("   Dashboard: http://localhost:8501")
    print("   API Docs:  http://localhost:8000/docs")
    
    print("\n4. 🧪 Run tests (optional):")
    print("   cd tests && python test_api.py")
    print("   cd tests && python test_nlp.py")
    
    print("\n📚 For more information, see README.md")
    print("\n⚠️  Note: First-time model downloads may take several minutes")
    print("="*60)

def main():
    """Main setup function"""
    print("🚀 EquityAI Research Tool Setup")
    print("="*50)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Virtual Environment", create_virtual_environment),
        ("Dependencies", install_dependencies),
        ("NLP Models", download_nlp_models),
        ("Environment File", setup_environment_file),
        ("Directories", create_directories),
        ("Installation Test", test_installation),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please resolve the error and try again")
            sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main()
