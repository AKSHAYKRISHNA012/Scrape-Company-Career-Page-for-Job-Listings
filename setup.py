"""
Setup and Quick Start Script for Job Scraper
Run this to verify your environment and execute the scraper
"""
import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.7+")
        return False

def install_requirements():
    """Install required packages"""
    try:
        print("📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def run_scraper():
    """Run the main scraper"""
    try:
        print("🚀 Running the job scraper...")
        subprocess.check_call([sys.executable, "real_microsoft_jobs_scraper.py"])
        print("✅ Scraper completed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Scraper failed to run")
        return False

def main():
    """Main setup function"""
    print("🔧 Job Scraper Setup & Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Run scraper
    if not run_scraper():
        return False
    
    # Check output files
    output_files = ["Microsoft_Jobs.xlsx"]
    for file in output_files:
        if os.path.exists(file):
            print(f"✅ Output file created: {file}")
        else:
            print(f"❌ Output file missing: {file}")
    
    print("\n🎉 Setup completed successfully!")
    print("📁 Check your Excel files for the scraped job data")
    print("🚀 Ready to upload to GitHub with hashtag #cl-genai-jobscraper")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
