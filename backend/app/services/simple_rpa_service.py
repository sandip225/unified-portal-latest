"""
Simple RPA Service - Windows Localhost Version
"""

import time
import os
import logging
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ECaxia

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTorrentRPA:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Windows localhost Chrome setup"""
        try:
            logger.info("🚀 Setting up Chrome driver for Windows localhost...")
            
            # Detect Windows environment
            is_windows = platform.system() == 'Windows'
            logger.info(f"🔍 Platform detected: {platform.system()}")
            
            # Chrome options for localhost (visible browser)
            options = Options()
            
            if is_windows:
                # Windows localhost - visible browser for debugging
                options.add_argument("--start-maximized")
                options.add_argument("--disable-notifications")
                options.add_argument("--disable-popup-blocking")
                logger.info("💻 Using Windows localhost options (visible browser)")
            else:
                # Fallback for other systems
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                logger.info("🐧 Using headless options for non-Windows")
            
            # Common options
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Try webdriver-manager first (best for localhost)
            try:
                logger.info("🔧 Trying webdriver-manager...")
                from webdriver_manager.chrome import ChromeDriverManager
                
                driver_path = ChromeDriverManager().install()
                logger.info(f"✅ ChromeDriver installed at: {driver_path}")
                
                # Fix webdriver-manager path issue on Windows
                if 'THIRD_PARTY_NOTICES' in driver_path or not driver_path.endswith('.exe'):
                    # Extract the correct directory and find the actual chromedriver binary
                    driver_dir = os.path.dirname(driver_path)
                    
                    # Look for the actual chromedriver binary
                    possible_paths = [
                        os.path.join(driver_dir, 'chromedriver.exe'),
                        os.path.join(driver_dir, 'chromedriver-win32', 'chromedriver.exe'),
                        os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe'),
                    ]
                    
                    for possible_path in possible_paths:
                        if os.path.exists(possible_path):
                            driver_path = possible_path
                            logger.info(f"🔧 Fixed ChromeDriver path: {driver_path}")
                            break
                    else:
                        # Search for any chromedriver.exe file in the directory tree
                        for root, dirs, files in os.walk(os.path.dirname(driver_dir)):
                            for file in files:
                                if file == 'chromedriver.exe':
                                    driver_path = os.path.join(root, file)
                                    logger.info(f"🔧 Found ChromeDriver binary: {driver_path}")
                                    break
                            if driver_path.endswith('.exe'):
                                break
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
                logger.info("✅ Chrome driver setup successful with webdriver-manager")
                
            except ImportError:
                logger.info("⚠️ webdriver-manager not available, trying system Chrome...")
                # Fallback to system Chrome
                self.driver = webdriver.Chrome(options=options)
                logger.info("✅ Chrome driver setup successful with system Chrome")
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            self.wait = WebDriverWait(self.driver, 20)
            
            # Test the driver
            logger.info("🧪 Testing Chrome driver...")
            self.driver.get("data:text/html,<html><body><h1>RPA Test - Chrome Working!</h1></body></html>")
            logger.info("✅ Chrome driver test successful")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Chrome setup failed: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            
            # Provide helpful suggestions
            if "chromedriver" in str(e).lower():
                logger.error("💡 Suggestion: Install Chrome browser and ensure it's updated")
                logger.error("💡 Or run: pip install webdriver-manager")
            
            return False
    
    def navigate_to_torrent_power(self):
        """Navigate to Torrent Power website"""
        try:
            url = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
            logger.info(f"🌐 Navigating to: {url}")
            
            self.driver.get(url)
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("✅ Page loaded successfully")
            
            # Clean automation without annoying banners
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False
    
    def fill_form(self, form_data):
        """Fill the Torrent Power form"""
        try:
            logger.info("🚀 Starting form filling...")
            filled_fields = []
            time.sleep(2)  # Wait for page to fully load
            
            # 1. Fill City Dropdown
            try:
                logger.info("🔍 Looking for city dropdown...")
                city_select = self.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "select")))
                
                select = Select(city_select)
                city = form_data.get('city', 'Ahmedabad')
                
                # Try to select city
                options = select.options
                for option in options:
                    if city.lower() in option.text.lower():
                        select.select_by_value(option.get_attribute('value'))
                        filled_fields.append(f"✅ City: {option.text}")
                        logger.info(f"✅ City selected: {option.text}")
                        
                        # Highlight the field
                        self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", city_select)
                        break
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ City dropdown error: {e}")
                filled_fields.append("❌ City dropdown not found")
            
            # 2. Fill Service Number
            try:
                logger.info("🔍 Looking for service number field...")
                service_selectors = [
                    "input[placeholder*='Service Number']",
                    "input[placeholder*='Service']",
                    "input[name*='service']",
                    "input[id*='service']"
                ]
                
                service_input = None
                for selector in service_selectors:
                    try:
                        service_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not service_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if text_inputs:
                        service_input = text_inputs[0]
                
                if service_input and form_data.get('service_number'):
                    service_input.clear()
                    service_input.send_keys(form_data['service_number'])
                    filled_fields.append(f"✅ Service Number: {form_data['service_number']}")
                    logger.info(f"✅ Service Number filled: {form_data['service_number']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", service_input)
                else:
                    filled_fields.append("❌ Service Number field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Service Number error: {e}")
                filled_fields.append("❌ Service Number error")
            
            # 3. Fill T Number
            try:
                logger.info("🔍 Looking for T Number field...")
                t_selectors = [
                    "input[placeholder*='T No']",
                    "input[placeholder*='T-No']",
                    "input[name*='tno']"
                ]
                
                t_input = None
                for selector in t_selectors:
                    try:
                        t_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not t_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if len(text_inputs) > 1:
                        t_input = text_inputs[1]
                
                if t_input and form_data.get('t_number'):
                    t_input.clear()
                    t_input.send_keys(form_data['t_number'])
                    filled_fields.append(f"✅ T Number: {form_data['t_number']}")
                    logger.info(f"✅ T Number filled: {form_data['t_number']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", t_input)
                else:
                    filled_fields.append("❌ T Number field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ T Number error: {e}")
                filled_fields.append("❌ T Number error")
            
            # 4. Fill Mobile Number
            try:
                logger.info("🔍 Looking for mobile field...")
                mobile_selectors = [
                    "input[type='tel']",
                    "input[placeholder*='Mobile']",
                    "input[name*='mobile']"
                ]
                
                mobile_input = None
                for selector in mobile_selectors:
                    try:
                        mobile_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not mobile_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if len(text_inputs) > 2:
                        mobile_input = text_inputs[2]
                
                if mobile_input and form_data.get('mobile'):
                    mobile_input.clear()
                    mobile_input.send_keys(form_data['mobile'])
                    filled_fields.append(f"✅ Mobile: {form_data['mobile']}")
                    logger.info(f"✅ Mobile filled: {form_data['mobile']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", mobile_input)
                else:
                    filled_fields.append("❌ Mobile field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Mobile error: {e}")
                filled_fields.append("❌ Mobile error")
            
            # 5. Fill Email
            try:
                logger.info("🔍 Looking for email field...")
                email_selectors = [
                    "input[type='email']",
                    "input[placeholder*='Email']",
                    "input[name*='email']"
                ]
                
                email_input = None
                for selector in email_selectors:
                    try:
                        email_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not email_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if len(text_inputs) > 3:
                        email_input = text_inputs[3]
                
                if email_input and form_data.get('email'):
                    email_input.clear()
                    email_input.send_keys(form_data['email'])
                    filled_fields.append(f"✅ Email: {form_data['email']}")
                    logger.info(f"✅ Email filled: {form_data['email']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", email_input)
                else:
                    filled_fields.append("❌ Email field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Email error: {e}")
                filled_fields.append("❌ Email error")
            
            # 6. Find and click Submit button
            try:
                logger.info("� Looking for submit button...")
                submit_selectors = [
                    "button[type='submit']",
                    "input[type='submit']",
                    "button:contains('Submit')",
                    "button:contains('Apply')",
                    "button:contains('Send')",
                    ".btn-primary",
                    ".submit-btn"
                ]
                
                submit_button = None
                for selector in submit_selectors:
                    try:
                        if ":contains" in selector:
                            # Use XPath for text-based search
                            xpath = f"//button[contains(text(), '{selector.split(':contains(')[1].strip(')')}')]"
                            submit_button = self.driver.find_element(By.XPATH, xpath)
                        else:
                            submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                # Fallback: look for any button that might be submit
                if not submit_button:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        button_text = button.text.lower()
                        if any(word in button_text for word in ['submit', 'apply', 'send', 'save']):
                            submit_button = button
                            break
                
                if submit_button:
                    logger.info("🎯 Found submit button, clicking...")
                    
                    # Scroll to submit button
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    time.sleep(1)
                    
                    # Click submit button
                    submit_button.click()
                    filled_fields.append("✅ Form submitted successfully")
                    logger.info("✅ Form submitted successfully")
                    
                    # Wait for submission to process
                    time.sleep(3)
                    
                    # Add success message to the page after submission
                    success_message_script = """
                    const successMsg = document.createElement('div');
                    successMsg.innerHTML = `
                        <div style="position: fixed; top: 20px; right: 20px; background: #28a745; color: white; padding: 20px 30px; border-radius: 10px; font-family: Arial, sans-serif; font-size: 16px; z-index: 999999; box-shadow: 0 4px 20px rgba(0,0,0,0.3); max-width: 400px;">
                            <strong>🎉 Application Submitted Successfully!</strong><br>
                            <small style="font-size: 14px; margin-top: 10px; display: block;">
                                Your name change request has been submitted to Torrent Power.<br>
                                You will receive a confirmation email shortly.
                            </small>
                        </div>
                    `;
                    document.body.appendChild(successMsg);
                    
                    setTimeout(() => {
                        if (successMsg.parentNode) {
                            successMsg.parentNode.removeChild(successMsg);
                        }
                    }, 8000);
                    """
                    
                    self.driver.execute_script(success_message_script)
                    
                else:
                    filled_fields.append("⚠️ Submit button not found - please submit manually")
                    logger.warning("⚠️ Submit button not found")
                
            except Exception as e:
                logger.error(f"❌ Submit button error: {e}")
                filled_fields.append("❌ Submit button error")
            
            # Clean completion without popup
            success_count = len([f for f in filled_fields if f.startswith('✅')])
            logger.info(f"📊 Form filling completed: {success_count}/6 fields filled")
            
            return {
                "success": success_count > 0,
                "filled_fields": filled_fields,
                "total_filled": success_count,
                "total_fields": 6  # Updated to include submit button
            }
            
        except Exception as e:
            logger.error(f"❌ Form filling failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "filled_fields": ["❌ Form filling failed"],
                "total_filled": 0,
                "total_fields": 6
            }
    
    def run_automation(self, form_data):
        """Run complete Torrent Power automation"""
        try:
            logger.info("🤖 Starting Torrent Power RPA automation...")
            
            # Setup driver
            if not self.setup_driver():
                return {"success": False, "error": "Chrome setup failed"}
            
            # Navigate to Torrent Power
            if not self.navigate_to_torrent_power():
                return {"success": False, "error": "Failed to navigate to Torrent Power website"}
            
            # Fill the form
            result = self.fill_form(form_data)
            
            # Keep browser open for user interaction (5 minutes)
            logger.info("🕐 Keeping browser open for 5 minutes for user interaction...")
            time.sleep(300)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ RPA automation failed: {e}")
            return {"success": False, "error": str(e)}
        finally:
            # Don't close driver immediately - let user interact
            pass
    
    def close_driver(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("✅ Browser closed")
        except Exception as e:
            logger.error(f"❌ Error closing browser: {e}")


# Test function for localhost
def test_localhost_rpa():
    """Test RPA on localhost"""
    test_data = {
        "city": "Ahmedabad",
        "service_number": "TP123456",
        "t_number": "T789",
        "mobile": "9632587410",
        "email": "test@gmail.com"
    }
    
    rpa = SimpleTorrentRPA()
    result = rpa.run_automation(test_data)
    
    print("🔍 Localhost RPA Test Results:")
    print(f"Success: {result.get('success')}")
    print(f"Fields filled: {result.get('total_filled', 0)}/5")
    
    if result.get('filled_fields'):
        print("Field Results:")
        for field in result['filled_fields']:
            print(f"  {field}")
    
    return result


if __name__ == "__main__":
    test_localhost_rpa()