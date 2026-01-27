"""
Enhanced Selenium Service with advanced automation features
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from typing import Dict, Any, Optional, List
import json
import os
from datetime import datetime
import base64
from PIL import Image
import io

logger = logging.getLogger(__name__)

class EnhancedSeleniumService:
    """Enhanced Selenium service with advanced automation capabilities"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.actions = None
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("automation_logs", exist_ok=True)
    
    def setup_driver(self, headless: bool = False, mobile_emulation: bool = False) -> webdriver.Chrome:
        """Setup Chrome WebDriver with enhanced options"""
        chrome_options = Options()
        
        # Mobile emulation for responsive testing
        if mobile_emulation:
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        if headless:
            chrome_options.add_argument('--headless')
        
        # Enhanced Chrome options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Performance optimizations
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Faster loading
        chrome_options.add_argument('--disable-javascript')  # For simple form filling
        
        # Stealth mode to avoid detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            self.actions = ActionChains(self.driver)
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return self.driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise e
    
    def smart_wait_and_fill(self, locator: tuple, value: str, clear_first: bool = True) -> bool:
        """Smart form filling with multiple wait strategies"""
        try:
            # Wait for element to be present
            element = self.wait.until(EC.presence_of_element_located(locator))
            
            # Wait for element to be clickable
            element = self.wait.until(EC.element_to_be_clickable(locator))
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Clear field if requested
            if clear_first:
                element.clear()
                time.sleep(0.2)
            
            # Type with human-like delays
            for char in value:
                element.send_keys(char)
                time.sleep(0.05)  # Human-like typing speed
            
            logger.info(f"Successfully filled field with value: {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to fill field: {e}")
            return False
    
    def smart_select_dropdown(self, locator: tuple, value: str, by_value: bool = False) -> bool:
        """Smart dropdown selection with fallback strategies"""
        try:
            select_element = Select(self.wait.until(EC.element_to_be_clickable(locator)))
            
            if by_value:
                select_element.select_by_value(value)
            else:
                # Try visible text first
                try:
                    select_element.select_by_visible_text(value)
                except:
                    # Fallback to partial text match
                    options = select_element.options
                    for option in options:
                        if value.lower() in option.text.lower():
                            select_element.select_by_visible_text(option.text)
                            break
            
            logger.info(f"Successfully selected dropdown value: {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to select dropdown: {e}")
            return False
    
    def take_full_page_screenshot(self, filename: str) -> str:
        """Take full page screenshot including scrollable content"""
        try:
            # Get page dimensions
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Take screenshots of each viewport
            screenshots = []
            scroll_position = 0
            
            while scroll_position < total_height:
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position})")
                time.sleep(0.5)
                
                screenshot = self.driver.get_screenshot_as_png()
                screenshots.append(Image.open(io.BytesIO(screenshot)))
                
                scroll_position += viewport_height
            
            # Combine screenshots
            if screenshots:
                total_width = screenshots[0].width
                combined_height = sum(img.height for img in screenshots)
                
                combined_image = Image.new('RGB', (total_width, combined_height))
                y_offset = 0
                
                for img in screenshots:
                    combined_image.paste(img, (0, y_offset))
                    y_offset += img.height
                
                combined_image.save(filename)
                logger.info(f"Full page screenshot saved: {filename}")
                return filename
            
        except Exception as e:
            logger.error(f"Failed to take full page screenshot: {e}")
            # Fallback to regular screenshot
            return self.take_screenshot(filename)
    
    def take_screenshot(self, filename: str) -> str:
        """Take regular screenshot"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Could not take screenshot: {e}")
            return None
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """Wait for page to fully load"""
        try:
            # Wait for document ready state
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            # Wait for jQuery if present
            try:
                self.wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))
            except:
                pass  # jQuery not present
            
            return True
        except Exception as e:
            logger.warning(f"Page load timeout: {e}")
            return False
    
    def extract_form_data(self) -> Dict[str, Any]:
        """Extract all form data from current page"""
        try:
            form_data = {}
            
            # Extract input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for input_elem in inputs:
                name = input_elem.get_attribute("name") or input_elem.get_attribute("id")
                value = input_elem.get_attribute("value")
                input_type = input_elem.get_attribute("type")
                
                if name and input_type not in ["submit", "button", "hidden"]:
                    form_data[name] = value
            
            # Extract select fields
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for select_elem in selects:
                name = select_elem.get_attribute("name") or select_elem.get_attribute("id")
                if name:
                    select_obj = Select(select_elem)
                    try:
                        selected_option = select_obj.first_selected_option
                        form_data[name] = selected_option.text
                    except:
                        form_data[name] = ""
            
            # Extract textarea fields
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            for textarea in textareas:
                name = textarea.get_attribute("name") or textarea.get_attribute("id")
                value = textarea.get_attribute("value") or textarea.text
                if name:
                    form_data[name] = value
            
            return form_data
            
        except Exception as e:
            logger.error(f"Failed to extract form data: {e}")
            return {}
    
    def validate_form_submission(self, expected_elements: List[str]) -> Dict[str, bool]:
        """Validate form submission by checking for expected elements"""
        validation_results = {}
        
        for element_selector in expected_elements:
            try:
                # Try different selector types
                if element_selector.startswith("#"):
                    element = self.driver.find_element(By.ID, element_selector[1:])
                elif element_selector.startswith("."):
                    element = self.driver.find_element(By.CLASS_NAME, element_selector[1:])
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, element_selector)
                
                validation_results[element_selector] = element.is_displayed()
                
            except:
                validation_results[element_selector] = False
        
        return validation_results
    
    def create_automation_report(self, service_name: str, data: Dict[str, Any], 
                               result: Dict[str, Any]) -> str:
        """Create detailed automation report"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "service_name": service_name,
                "input_data": data,
                "result": result,
                "browser_info": {
                    "user_agent": self.driver.execute_script("return navigator.userAgent"),
                    "window_size": self.driver.get_window_size(),
                    "current_url": self.driver.current_url
                },
                "page_source_length": len(self.driver.page_source),
                "cookies": self.driver.get_cookies()
            }
            
            report_filename = f"automation_logs/{service_name}_{int(time.time())}.json"
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Automation report saved: {report_filename}")
            return report_filename
            
        except Exception as e:
            logger.error(f"Failed to create automation report: {e}")
            return None
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            self.actions = None

# Global enhanced service instance
enhanced_selenium_service = EnhancedSeleniumService()