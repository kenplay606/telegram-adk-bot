"""
AI Agency Suite - Setup Script
SECURITY: Never logs or stores API keys
"""
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required. You have {version.major}.{version.minor}")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")


def install_requirements():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def check_ollama():
    """Check if Ollama is installed"""
    print("\nChecking for Ollama...")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Ollama is installed")
            return True
        else:
            print("⚠️  Ollama not found")
            return False
    except FileNotFoundError:
        print("⚠️  Ollama not found")
        return False


def install_ollama():
    """Provide instructions for installing Ollama"""
    print("\n" + "!" * 60)
    print("  OLLAMA INSTALLATION REQUIRED")
    print("!" * 60)
    
    system = platform.system()
    
    if system == "Windows":
        print("\nDownload and install Ollama for Windows:")
        print("https://ollama.ai/download/windows")
    elif system == "Darwin":  # macOS
        print("\nInstall Ollama on macOS:")
        print("brew install ollama")
        print("\nOr download from: https://ollama.ai/download/mac")
    else:  # Linux
        print("\nInstall Ollama on Linux:")
        print("curl -fsSL https://ollama.ai/install.sh | sh")
    
    print("\nAfter installing Ollama, run this setup script again.")
    
    choice = input("\nContinue anyway? (y/n): ")
    if choice.lower() != 'y':
        sys.exit(0)


def pull_ollama_model():
    """Pull default Ollama model"""
    print("\nPulling Ollama model (llama3.1)...")
    print("This may take a few minutes...")
    
    try:
        subprocess.check_call(["ollama", "pull", "llama3.1"])
        print("✅ Model downloaded")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to pull model. You can do this manually later:")
        print("   ollama pull llama3.1")


def initialize_database():
    """Initialize database"""
    print("\nInitializing database...")
    
    try:
        from backend.core.db_client import init_db
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")


def create_env_file():
    """Create .env file from .env.example"""
    print("\nSetting up environment file...")
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        choice = input("Overwrite? (y/n): ")
        if choice.lower() != 'y':
            print("Keeping existing .env file")
            return
    
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from .env.example")
        print("\n" + "!" * 60)
        print("  IMPORTANT: Configure your .env file")
        print("!" * 60)
        print("\nEdit .env and add your API keys (optional):")
        print("- INSTAGRAM_ACCESS_TOKEN (for client DM automation)")
        print("- YOUTUBE_API_KEY (for posting Shorts)")
        print("- FACEBOOK_ACCESS_TOKEN (for posting videos)")
        print("- GROQ_API_KEY (optional cloud AI)")
        print("\nThe system will work locally without these keys.")
    else:
        print("❌ .env.example not found")


def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    dirs = [
        "data",
        "videos",
        "thumbnails",
        "logs",
        "uploads",
        "temp_videos",
        "output",
        "chroma_db",
        "websites"
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created")


def print_next_steps():
    """Print next steps"""
    print_header("SETUP COMPLETE!")
    
    print("Next steps:\n")
    
    print("1. Configure API keys (optional):")
    print("   Edit .env file and add your API keys\n")
    
    print("2. Start the system:")
    print("   python run.py\n")
    
    print("3. Access the dashboard:")
    print("   Open http://localhost:8501 in your browser\n")
    
    print("4. Access the API:")
    print("   Open http://localhost:8000/docs for API documentation\n")
    
    print("For deployment instructions, see DEPLOYMENT.md\n")


def main():
    """Main setup function"""
    print_header("AI AGENCY SUITE - SETUP")
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_requirements()
    
    # Check Ollama
    if not check_ollama():
        install_ollama()
        
        # Check again after instructions
        if check_ollama():
            pull_ollama_model()
    else:
        pull_ollama_model()
    
    # Create directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    # Create .env file
    create_env_file()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
