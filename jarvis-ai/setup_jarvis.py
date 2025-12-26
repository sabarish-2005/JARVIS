"""
==================== JARVIS SETUP SCRIPT ====================
Quick setup and dependency installation
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    """Run shell command with output"""
    print(f"→ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print_header("JARVIS AI - PRODUCTION SETUP")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Install requirements
    print_header("Installing Python Dependencies")
    
    req_file = Path(__file__).parent / "requirements-python.txt"
    if not req_file.exists():
        print("❌ requirements-python.txt not found!")
        sys.exit(1)
    
    run_command(
        f'pip install -r "{req_file}"',
        "Installing Python packages"
    )
    
    # Install Playwright browsers
    print_header("Installing Playwright Browsers")
    run_command(
        "playwright install chromium",
        "Installing Chromium for automation"
    )
    
    # Create .env file if not exists
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print_header("Creating .env File")
        with open(env_file, 'w') as f:
            f.write("# JARVIS AI - Environment Variables\n")
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
            f.write("OPENAI_API_KEY=optional_openai_key\n")
        print("✅ .env file created")
        print("⚠️  Please edit .env and add your GROQ_API_KEY")
    
    # Create logs directory
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory ready")
    
    print_header("SETUP COMPLETE!")
    print("Next steps:")
    print("1. Edit .env file and add your GROQ_API_KEY")
    print("2. Run: python jarvis_main.py")
    print("3. Say: 'JARVIS' followed by your command")
    print("\n🚀 JARVIS is ready to serve, Sir!")

if __name__ == "__main__":
    main()
