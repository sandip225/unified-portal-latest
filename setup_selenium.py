#!/usr/bin/env python3
"""
Selenium Setup Script for Gujarat Unified Portal
Installs and configures Selenium with all dependencies
"""
import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and handle errors"""
    try:
        logger.info(f"Running: {description}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install Python requirements"""
    logger.info("📦 Installing Python requirements...")
    
    requirements = [
        "selenium==4.26.1",
        "webdriver-manager==4.0.2", 
        "undetected-chromedriver==3.5.5",
        "selenium-stealth==1.0.6",
        "fake-useragent==1.4.0"
    ]
    
    for requirement in requirements:
        if not run_command(f"pip install {requirement}", f"Installing {requirement}"):
            return False
    
    return True

def check_chrome_installation():
    """Check if Chrome is installed"""
    system = platform.system()
    
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
    elif system == "Darwin":  # macOS
        chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    else:  # Linux
        chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
    
    for path in chrome_paths:
        if os.path.exists(path):
            logger.info(f"✅ Chrome found at: {path}")
            return True
    
    logger.warning("⚠️ Chrome not found. Please install Chrome manually.")
    return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "chrome_automation_data",
        "downloads", 
        "screenshots",
        "user_data",
        "automation_logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")
    
    return True

def test_selenium_setup():
    """Test Selenium setup"""
    logger.info("🧪 Testing Selenium setup...")
    
    test_script = """
import sys
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    import undetected_chromedriver as uc
    from selenium_stealth import stealth
    from fake_useragent import UserAgent
    
    print("✅ All Selenium imports successful")
    
    # Test ChromeDriver download
    driver_path = ChromeDriverManager().install()
    print(f"✅ ChromeDriver installed at: {driver_path}")
    
    # Test basic Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    print("✅ Chrome options configured")
    
    # Test UserAgent
    ua = UserAgent()
    user_agent = ua.random
    print(f"✅ Random user agent: {user_agent[:50]}...")
    
    print("🎉 Selenium setup test completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Setup test failed: {e}")
    sys.exit(1)
"""
    
    try:
        exec(test_script)
        return True
    except Exception as e:
        logger.error(f"❌ Selenium test failed: {e}")
        return False

def create_selenium_config():
    """Create Selenium configuration file"""
    config_content = """
# Selenium Configuration for Gujarat Unified Portal

## Installed Components:
- Selenium WebDriver 4.26.1
- WebDriver Manager 4.0.2
- Undetected ChromeDriver 3.5.5
- Selenium Stealth 1.0.6
- Fake UserAgent 1.4.0

## Features:
- ✅ Anti-detection stealth mode
- ✅ Undetected ChromeDriver support
- ✅ User data persistence
- ✅ Government site optimization
- ✅ Smart element finding
- ✅ Human-like typing simulation
- ✅ Multiple click strategies
- ✅ Automatic screenshot capture

## API Endpoints:
- GET /api/selenium/health - Check Selenium health
- POST /api/selenium/test-driver - Test WebDriver
- GET /api/selenium/config - Get configuration
- POST /api/selenium/install-chrome - Chrome installation guide
- DELETE /api/selenium/cleanup - Cleanup data

## Usage:
1. Start your FastAPI server: uvicorn app.main:app --reload
2. Visit http://localhost:8000/docs for API documentation
3. Test Selenium health: GET /api/selenium/health
4. Run automation: POST /api/unified-automation/start-automation

## Troubleshooting:
- If Chrome not found, install from https://www.google.com/chrome/
- If ChromeDriver issues, delete chrome_automation_data folder
- Check logs in automation_logs directory
- Use headless=False to see browser in action
"""
    
    with open("SELENIUM_SETUP.md", "w") as f:
        f.write(config_content)
    
    logger.info("✅ Created SELENIUM_SETUP.md configuration file")
    return True

def main():
    """Main setup function"""
    logger.info("🚀 Starting Selenium setup for Gujarat Unified Portal...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        logger.error("❌ Failed to install requirements")
        sys.exit(1)
    
    # Check Chrome installation
    chrome_installed = check_chrome_installation()
    if not chrome_installed:
        logger.warning("⚠️ Chrome not found. Automation may not work without Chrome.")
        logger.info("📥 Install Chrome from: https://www.google.com/chrome/")
    
    # Create directories
    if not create_directories():
        logger.error("❌ Failed to create directories")
        sys.exit(1)
    
    # Test Selenium setup
    if not test_selenium_setup():
        logger.error("❌ Selenium setup test failed")
        sys.exit(1)
    
    # Create configuration
    if not create_selenium_config():
        logger.error("❌ Failed to create configuration")
        sys.exit(1)
    
    logger.info("🎉 Selenium setup completed successfully!")
    logger.info("📋 Next steps:")
    logger.info("   1. Start your FastAPI server: uvicorn app.main:app --reload")
    logger.info("   2. Test health check: GET http://localhost:8000/api/selenium/health")
    logger.info("   3. Run automation: POST http://localhost:8000/api/unified-automation/start-automation")
    
    if not chrome_installed:
        logger.info("   4. Install Chrome from: https://www.google.com/chrome/")

if __name__ == "__main__":
    main()