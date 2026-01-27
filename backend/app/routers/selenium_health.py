"""
Selenium Health Check and Configuration API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from ..services.selenium_config import selenium_config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/selenium", tags=["selenium-health"])

class SeleniumTestRequest(BaseModel):
    url: str = "https://www.google.com"
    headless: bool = True
    stealth_mode: bool = True
    undetected: bool = False

class SeleniumHealthResponse(BaseModel):
    status: str
    chrome_installed: bool
    driver_available: bool
    chrome_version: Optional[str] = None
    driver_path: Optional[str] = None
    platform: str
    directories: Dict[str, str]
    timestamp: str

@router.get("/health", response_model=SeleniumHealthResponse)
async def selenium_health_check():
    """Check Selenium and Chrome installation status"""
    try:
        # Check Chrome installation
        chrome_info = selenium_config.check_chrome_installation()
        
        return SeleniumHealthResponse(
            status="healthy" if chrome_info.get("chrome_installed") and chrome_info.get("driver_available") else "unhealthy",
            chrome_installed=chrome_info.get("chrome_installed", False),
            driver_available=chrome_info.get("driver_available", False),
            chrome_version=chrome_info.get("chrome_version"),
            driver_path=chrome_info.get("driver_path"),
            platform=chrome_info.get("platform", "unknown"),
            directories={
                "user_data": chrome_info.get("user_data_dir", ""),
                "downloads": chrome_info.get("downloads_dir", ""),
                "screenshots": chrome_info.get("screenshots_dir", "")
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Selenium health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-driver")
async def test_selenium_driver(request: SeleniumTestRequest):
    """Test Selenium WebDriver functionality"""
    driver = None
    try:
        logger.info(f"Testing Selenium driver with URL: {request.url}")
        
        # Create driver
        driver = selenium_config.create_driver(
            headless=request.headless,
            stealth_mode=request.stealth_mode,
            undetected=request.undetected
        )
        
        # Navigate to test URL
        driver.get(request.url)
        
        # Get page information
        page_info = {
            "title": driver.title,
            "url": driver.current_url,
            "page_source_length": len(driver.page_source),
            "window_size": driver.get_window_size(),
            "user_agent": driver.execute_script("return navigator.userAgent")
        }
        
        # Take screenshot
        screenshot_path = selenium_config.take_screenshot(driver, "test_screenshot.png")
        
        # Get driver info
        driver_info = selenium_config.get_driver_info(driver)
        
        return {
            "success": True,
            "message": "Selenium driver test completed successfully",
            "page_info": page_info,
            "driver_info": driver_info,
            "screenshot_path": screenshot_path,
            "test_config": {
                "headless": request.headless,
                "stealth_mode": request.stealth_mode,
                "undetected": request.undetected
            }
        }
        
    except Exception as e:
        logger.error(f"Selenium driver test failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Selenium driver test failed"
        }
        
    finally:
        # Cleanup driver
        if driver:
            selenium_config.cleanup_driver(driver)

@router.get("/config")
async def get_selenium_config():
    """Get current Selenium configuration"""
    try:
        chrome_info = selenium_config.check_chrome_installation()
        
        return {
            "selenium_version": "4.26.1",
            "webdriver_manager_version": "4.0.2",
            "undetected_chromedriver_version": "3.5.5",
            "selenium_stealth_version": "1.0.6",
            "chrome_info": chrome_info,
            "default_options": {
                "headless": False,
                "stealth_mode": True,
                "undetected": False,
                "window_size": "1920x1080",
                "user_data_persistent": True,
                "anti_detection": True
            },
            "supported_features": [
                "Stealth mode",
                "Undetected Chrome",
                "User data persistence",
                "Anti-detection scripts",
                "Government site optimization",
                "Smart element finding",
                "Human-like typing",
                "Multiple click strategies",
                "Automatic screenshot capture"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get Selenium config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/install-chrome")
async def install_chrome_guide():
    """Provide Chrome installation guide"""
    try:
        import platform
        
        system = platform.system()
        
        if system == "Windows":
            guide = {
                "system": "Windows",
                "steps": [
                    "1. Download Chrome from https://www.google.com/chrome/",
                    "2. Run the installer as Administrator",
                    "3. Follow installation wizard",
                    "4. Restart your system",
                    "5. Test Selenium again"
                ],
                "download_url": "https://www.google.com/chrome/",
                "alternative": "Use Chocolatey: choco install googlechrome"
            }
        elif system == "Darwin":  # macOS
            guide = {
                "system": "macOS",
                "steps": [
                    "1. Download Chrome from https://www.google.com/chrome/",
                    "2. Open the .dmg file",
                    "3. Drag Chrome to Applications folder",
                    "4. Launch Chrome from Applications",
                    "5. Test Selenium again"
                ],
                "download_url": "https://www.google.com/chrome/",
                "alternative": "Use Homebrew: brew install --cask google-chrome"
            }
        else:  # Linux
            guide = {
                "system": "Linux",
                "steps": [
                    "1. Update package list: sudo apt update",
                    "2. Install Chrome: sudo apt install google-chrome-stable",
                    "3. Or download from https://www.google.com/chrome/",
                    "4. Install dependencies if needed",
                    "5. Test Selenium again"
                ],
                "download_url": "https://www.google.com/chrome/",
                "alternative": "Use snap: sudo snap install chromium"
            }
        
        return {
            "installation_guide": guide,
            "current_status": selenium_config.check_chrome_installation(),
            "note": "Chrome is required for Selenium automation to work properly"
        }
        
    except Exception as e:
        logger.error(f"Failed to provide Chrome installation guide: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup")
async def cleanup_selenium_data():
    """Cleanup Selenium data directories"""
    try:
        import shutil
        
        cleanup_results = {
            "user_data_cleaned": False,
            "downloads_cleaned": False,
            "screenshots_cleaned": False,
            "errors": []
        }
        
        # Cleanup user data directory
        try:
            if os.path.exists(selenium_config.chrome_user_data_dir):
                shutil.rmtree(selenium_config.chrome_user_data_dir)
                os.makedirs(selenium_config.chrome_user_data_dir, exist_ok=True)
                cleanup_results["user_data_cleaned"] = True
        except Exception as e:
            cleanup_results["errors"].append(f"User data cleanup failed: {e}")
        
        # Cleanup downloads directory
        try:
            if os.path.exists(selenium_config.downloads_dir):
                for file in os.listdir(selenium_config.downloads_dir):
                    file_path = os.path.join(selenium_config.downloads_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                cleanup_results["downloads_cleaned"] = True
        except Exception as e:
            cleanup_results["errors"].append(f"Downloads cleanup failed: {e}")
        
        # Cleanup old screenshots (keep last 10)
        try:
            if os.path.exists(selenium_config.screenshots_dir):
                screenshots = [f for f in os.listdir(selenium_config.screenshots_dir) if f.endswith('.png')]
                screenshots.sort(key=lambda x: os.path.getctime(os.path.join(selenium_config.screenshots_dir, x)))
                
                if len(screenshots) > 10:
                    for screenshot in screenshots[:-10]:
                        os.remove(os.path.join(selenium_config.screenshots_dir, screenshot))
                
                cleanup_results["screenshots_cleaned"] = True
        except Exception as e:
            cleanup_results["errors"].append(f"Screenshots cleanup failed: {e}")
        
        return {
            "success": len(cleanup_results["errors"]) == 0,
            "message": "Selenium data cleanup completed",
            "results": cleanup_results
        }
        
    except Exception as e:
        logger.error(f"Selenium cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))