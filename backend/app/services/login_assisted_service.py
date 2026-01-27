"""
Login Assisted Service for websites that require authentication
These websites need login first, then navigate to name change page
User handles: Login, CAPTCHA, OTP
Selenium handles: Form filling after login
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from typing import Dict, Any, Optional
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class LoginAssistedService:
    """Service for websites that require login - User handles auth, Selenium handles form filling"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        os.makedirs("screenshots", exist_ok=True)
    
    def setup_driver(self, headless: bool = False) -> webdriver.Chrome:
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        
        # Never use headless for login-required sites (user needs to see)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1200,800')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            return self.driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise e
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None

    # ELECTRICITY SERVICES - LOGIN REQUIRED
    
    def assist_guvnl_login_and_fill(self, data: Dict[str, Any], service_type: str) -> Dict[str, Any]:
        """
        GUVNL Portal (PGVCL, UGVCL, MGVCL, DGVCL) - Login required
        User handles: Login, CAPTCHA, OTP
        Selenium handles: Navigation to name change page and form filling
        """
        try:
            logger.info(f"Starting GUVNL {service_type} login assistance for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Navigate to GUVNL login page
            login_url = "https://portal.guvnl.in/login.php"
            self.driver.get(login_url)
            
            # Wait for login page
            self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            
            # Show instructions to user
            instruction_script = """
            alert(`🔐 LOGIN ASSISTANCE - GUVNL Portal
            
Please complete the following steps manually:
1. Enter your Consumer Number in Username field
2. Enter your Password (usually mobile number or bill number)
3. Solve the CAPTCHA
4. Click Login button
5. Complete OTP verification if required
6. Once logged in, click OK in this dialog

The system will then automatically navigate to name change page and fill your form.`);
            """
            self.driver.execute_script(instruction_script)
            
            # Wait for user to complete login (check for dashboard elements)
            logger.info("Waiting for user to complete login...")
            
            # Wait for successful login (look for dashboard or menu elements)
            try:
                # Wait for login success indicators
                self.wait.until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "dashboard")),
                    EC.presence_of_element_located((By.ID, "menu")),
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Name Change")),
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Services"))
                ))
                
                logger.info("Login successful! Navigating to name change page...")
                
                # Navigate to name change page
                try:
                    # Look for name change link in menu
                    name_change_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Name Change")
                    name_change_link.click()
                except:
                    # Alternative navigation
                    services_menu = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Services")
                    services_menu.click()
                    time.sleep(2)
                    name_change_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Name Change")
                    name_change_link.click()
                
                # Wait for name change form
                time.sleep(3)
                
                # Fill the form automatically
                filled_fields = self.fill_guvnl_name_change_form(data)
                
                screenshot_path = f"screenshots/guvnl_{service_type}_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                
                return {
                    "success": True,
                    "message": f"GUVNL {service_type} form filled successfully. Please review and submit manually.",
                    "screenshot_path": screenshot_path,
                    "filled_fields": filled_fields,
                    "website": f"GUVNL - {service_type}",
                    "next_step": "Review the filled form and click Submit button"
                }
                
            except Exception as login_wait_error:
                logger.warning(f"Login timeout or failed: {login_wait_error}")
                return {
                    "success": False,
                    "error": "Login timeout or failed",
                    "message": "Please complete login manually and try again",
                    "website": f"GUVNL - {service_type}"
                }
            
        except Exception as e:
            logger.error(f"GUVNL {service_type} assistance failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"GUVNL {service_type} assistance failed"
            }
        finally:
            # Keep browser open for manual verification
            pass
    
    def fill_guvnl_name_change_form(self, data: Dict[str, Any]) -> int:
        """Fill GUVNL name change form fields"""
        filled_count = 0
        
        try:
            # Consumer Number
            if data.get('consumer_number'):
                try:
                    consumer_field = self.driver.find_element(By.NAME, "consumer_no")
                    consumer_field.clear()
                    consumer_field.send_keys(data['consumer_number'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            # Old Name
            if data.get('old_name'):
                try:
                    old_name_field = self.driver.find_element(By.NAME, "old_name")
                    old_name_field.clear()
                    old_name_field.send_keys(data['old_name'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            # New Name
            if data.get('new_name'):
                try:
                    new_name_field = self.driver.find_element(By.NAME, "new_name")
                    new_name_field.clear()
                    new_name_field.send_keys(data['new_name'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            # Mobile Number
            if data.get('mobile'):
                try:
                    mobile_field = self.driver.find_element(By.NAME, "mobile")
                    mobile_field.clear()
                    mobile_field.send_keys(data['mobile'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            # Email
            if data.get('email'):
                try:
                    email_field = self.driver.find_element(By.NAME, "email")
                    email_field.clear()
                    email_field.send_keys(data['email'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            # Address
            if data.get('address'):
                try:
                    address_field = self.driver.find_element(By.NAME, "address")
                    address_field.clear()
                    address_field.send_keys(data['address'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            # Aadhar Number
            if data.get('aadhar_number'):
                try:
                    aadhar_field = self.driver.find_element(By.NAME, "aadhar")
                    aadhar_field.clear()
                    aadhar_field.send_keys(data['aadhar_number'])
                    filled_count += 1
                    time.sleep(0.5)
                except:
                    pass
            
            logger.info(f"Filled {filled_count} fields in GUVNL form")
            return filled_count
            
        except Exception as e:
            logger.error(f"Error filling GUVNL form: {e}")
            return filled_count
    
    # GAS SERVICES - LOGIN REQUIRED
    
    def assist_adani_gas_login_and_fill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adani Gas - Login required (Customer Portal + OTP)
        User handles: Login, OTP
        Selenium handles: Form filling after login
        """
        try:
            logger.info(f"Starting Adani Gas login assistance for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Navigate to Adani Gas customer portal
            login_url = "https://www.adanigas.com/myaccount"
            self.driver.get(login_url)
            
            # Wait for login page
            self.wait.until(EC.presence_of_element_located((By.ID, "login-form")))
            
            # Show instructions
            instruction_script = """
            alert(`🔐 LOGIN ASSISTANCE - Adani Gas Portal
            
Please complete the following steps manually:
1. Enter your Consumer Number
2. Enter your Mobile Number
3. Click "Send OTP" button
4. Enter the OTP received on your mobile
5. Click Login button
6. Once logged in, click OK in this dialog

The system will then navigate to name change section and fill your form.`);
            """
            self.driver.execute_script(instruction_script)
            
            # Wait for successful login
            try:
                self.wait.until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "customer-dashboard")),
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Name Transfer")),
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Services"))
                ))
                
                logger.info("Adani Gas login successful! Navigating to name change...")
                
                # Navigate to name change page
                name_change_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Name Transfer")
                name_change_link.click()
                
                time.sleep(3)
                
                # Fill form
                filled_fields = self.fill_adani_gas_form(data)
                
                screenshot_path = f"screenshots/adani_gas_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                
                return {
                    "success": True,
                    "message": "Adani Gas form filled successfully. Please review and submit.",
                    "screenshot_path": screenshot_path,
                    "filled_fields": filled_fields,
                    "website": "Adani Gas"
                }
                
            except Exception as login_error:
                return {
                    "success": False,
                    "error": "Login timeout or failed",
                    "message": "Please complete Adani Gas login and try again"
                }
            
        except Exception as e:
            logger.error(f"Adani Gas assistance failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    def fill_adani_gas_form(self, data: Dict[str, Any]) -> int:
        """Fill Adani Gas name change form"""
        filled_count = 0
        
        # Similar form filling logic for Adani Gas
        # Implementation details based on actual form structure
        
        return filled_count
    
    # WATER SERVICES - LOGIN REQUIRED
    
    def assist_municipal_water_login(self, data: Dict[str, Any], city: str) -> Dict[str, Any]:
        """
        Municipal Water Services (AMC, SMC, VMC, RMC) - Login/Ward verification required
        """
        try:
            logger.info(f"Starting {city} Municipal water login assistance")
            
            self.setup_driver(headless=False)
            
            # City-specific URLs
            city_urls = {
                "AMC": "https://ahmedabadcity.gov.in/citizen-services",
                "SMC": "https://www.suratmunicipal.gov.in/services",
                "VMC": "https://vmc.gov.in/citizen-services",
                "RMC": "https://www.rmc.gov.in/services"
            }
            
            url = city_urls.get(city, city_urls["AMC"])
            self.driver.get(url)
            
            # Show city-specific instructions
            instruction_script = f"""
            alert(`🔐 LOGIN ASSISTANCE - {city} Municipal Corporation
            
Please complete the following steps manually:
1. Navigate to Water Services section
2. Complete ward verification or login process
3. Enter your Connection ID/Consumer Number
4. Complete any required verification steps
5. Navigate to Name Change form
6. Click OK when ready for form filling

The system will then fill your form automatically.`);
            """
            self.driver.execute_script(instruction_script)
            
            # Wait for user to navigate to form
            time.sleep(10)  # Give user time to navigate
            
            # Try to fill form if available
            filled_fields = self.fill_municipal_water_form(data)
            
            screenshot_path = f"screenshots/{city.lower()}_water_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": f"{city} Municipal water form assistance completed",
                "screenshot_path": screenshot_path,
                "filled_fields": filled_fields,
                "website": f"{city} Municipal Corporation"
            }
            
        except Exception as e:
            logger.error(f"{city} Municipal assistance failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    def fill_municipal_water_form(self, data: Dict[str, Any]) -> int:
        """Fill municipal water form fields"""
        filled_count = 0
        
        # Generic form filling for municipal water services
        field_mappings = [
            ("connection_id", ["connection_id", "consumer_id", "connection_no"]),
            ("old_name", ["current_name", "old_name", "existing_name"]),
            ("new_name", ["new_name", "updated_name"]),
            ("mobile", ["mobile", "phone", "contact"]),
            ("address", ["address", "location"])
        ]
        
        for data_key, field_names in field_mappings:
            if data.get(data_key):
                for field_name in field_names:
                    try:
                        field = self.driver.find_element(By.NAME, field_name)
                        field.clear()
                        field.send_keys(data[data_key])
                        filled_count += 1
                        time.sleep(0.5)
                        break
                    except:
                        continue
        
        return filled_count

# Global service instance
login_assisted_service = LoginAssistedService()