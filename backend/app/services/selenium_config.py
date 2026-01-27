"""
Advanced Selenium Configuration Service
Handles Chrome setup, stealth mode, and anti-detection
"""
import os
import logging
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium_stealth import stealth
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SeleniumConfig:
    """Advanced Selenium configuration with anti-detection"""
    
    def __init__(self):
        self.user_agent = UserAgent()
        self.chrome_user_data_dir = os.path.join(os.getcwd(), "chrome_automation_data")
        self.downloads_dir = os.path.join(os.getcwd(), "downloads")
        self.screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        
        # Create directories
        os.makedirs(self.chrome_user_data_dir, exist_ok=True)
        os.makedirs(self.downloads_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def get_chrome_options(self, headless: bool = False, stealth_mode: bool = True) -> Options:
        """Get optimized Chrome options"""
        chrome_options = Options()
        
        # Basic options
        if headless:
            chrome_options.add_argument('--headless=new')  # New headless mode
        
        # Window and display options
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Performance options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Faster loading
        chrome_options.add_argument('--disable-javascript')  # For simple forms
        
        # Anti-detection options
        if stealth_mode:
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--no-service-autorun')
            chrome_options.add_argument('--password-store=basic')
        
        # User agent
        user_agent = self.user_agent.random
        chrome_options.add_argument(f'--user-agent={user_agent}')
        
        # User data directory for persistence
        chrome_options.add_argument(f'--user-data-dir={self.chrome_user_data_dir}')
        chrome_options.add_argument('--profile-directory=AutomationProfile')
        
        # Download preferences
        prefs = {
            "download.default_directory": self.downloads_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Platform-specific options
        if platform.system() == "Linux":
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--remote-debugging-port=9222')
        
        return chrome_options
    
    def create_driver(self, headless: bool = False, stealth_mode: bool = True, 
                     undetected: bool = False) -> webdriver.Chrome:
        """Create Chrome WebDriver with advanced configuration"""
        try:
            if undetected:
                # Use undetected-chromedriver for maximum stealth
                options = self.get_chrome_options(headless, stealth_mode)
                driver = uc.Chrome(options=options, version_main=None)
            else:
                # Use regular WebDriver with stealth configuration
                chrome_options = self.get_chrome_options(headless, stealth_mode)
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Apply stealth settings
            if stealth_mode:
                stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )
            
            # Execute additional anti-detection scripts
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": driver.execute_script("return navigator.userAgent").replace("Headless", "")
            })
            
            logger.info(f"Chrome WebDriver created successfully. Headless: {headless}, Stealth: {stealth_mode}")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to create Chrome WebDriver: {e}")
            raise e
    
    def configure_for_government_sites(self, driver: webdriver.Chrome) -> None:
        """Configure driver specifically for government websites"""
        try:
            # Set timeouts
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)
            
            # Execute government site specific configurations
            driver.execute_script("""
                // Disable console warnings
                console.warn = function() {};
                console.error = function() {};
                
                // Override automation detection
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Override chrome detection
                window.chrome = {
                    runtime: {},
                };
                
                // Override permissions
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({ state: 'granted' }),
                    }),
                });
                
                // Override plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            
            logger.info("Government site configurations applied")
            
        except Exception as e:
            logger.warning(f"Failed to apply government site configurations: {e}")
    
    def take_screenshot(self, driver: webdriver.Chrome, filename: str = None) -> str:
        """Take screenshot with automatic naming"""
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshot_path = os.path.join(self.screenshots_dir, filename)
            driver.save_screenshot(screenshot_path)
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def get_driver_info(self, driver: webdriver.Chrome) -> Dict[str, Any]:
        """Get driver and browser information"""
        try:
            info = {
                "browser_version": driver.capabilities.get('browserVersion'),
                "driver_version": driver.capabilities.get('chrome', {}).get('chromedriverVersion'),
                "platform": driver.capabilities.get('platformName'),
                "user_agent": driver.execute_script("return navigator.userAgent"),
                "window_size": driver.get_window_size(),
                "current_url": driver.current_url,
                "session_id": driver.session_id
            }
            return info
        except Exception as e:
            logger.error(f"Failed to get driver info: {e}")
            return {}
    
    def cleanup_driver(self, driver: webdriver.Chrome) -> None:
        """Safely cleanup driver resources"""
        try:
            if driver:
                driver.quit()
                logger.info("WebDriver cleaned up successfully")
        except Exception as e:
            logger.warning(f"Error during driver cleanup: {e}")
    
    def check_chrome_installation(self) -> Dict[str, Any]:
        """Check Chrome installation and version"""
        try:
            import subprocess
            
            # Check Chrome installation
            if platform.system() == "Windows":
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                ]
            elif platform.system() == "Darwin":  # macOS
                chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
            else:  # Linux
                chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
            
            chrome_installed = False
            chrome_version = None
            
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_installed = True
                    try:
                        if platform.system() == "Windows":
                            result = subprocess.run([path, "--version"], capture_output=True, text=True)
                        else:
                            result = subprocess.run([path, "--version"], capture_output=True, text=True)
                        chrome_version = result.stdout.strip()
                    except:
                        pass
                    break
            
            # Check ChromeDriver
            try:
                driver_path = ChromeDriverManager().install()
                driver_available = True
            except:
                driver_available = False
                driver_path = None
            
            return {
                "chrome_installed": chrome_installed,
                "chrome_version": chrome_version,
                "driver_available": driver_available,
                "driver_path": driver_path,
                "platform": platform.system(),
                "user_data_dir": self.chrome_user_data_dir,
                "downloads_dir": self.downloads_dir,
                "screenshots_dir": self.screenshots_dir
            }
            
        except Exception as e:
            logger.error(f"Failed to check Chrome installation: {e}")
            return {"error": str(e)}

# Global configuration instance
selenium_config = SeleniumConfig()