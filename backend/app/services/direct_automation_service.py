"""
Enhanced Direct Automation Service with Advanced Selenium Configuration
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from typing import Dict, Any, Optional
import os
from datetime import datetime

from .user_data_service import user_data_service
from .torrent_power_service import torrent_power_service

logger = logging.getLogger(__name__)

class EnhancedDirectAutomationService:
    """Enhanced service for direct automation with advanced Selenium configuration"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.actions = None
        self.current_user_key = None
        
    def setup_driver(self, headless: bool = False, stealth_mode: bool = True, 
                    undetected: bool = False) -> webdriver.Chrome:
        """Setup Chrome WebDriver with advanced configuration"""
        try:
            # Create driver using selenium_config
            self.driver = selenium_config.create_driver(
                headless=headless, 
                stealth_mode=stealth_mode, 
                undetected=undetected
            )
            
            # Configure for government sites
            selenium_config.configure_for_government_sites(self.driver)
            
            # Setup WebDriverWait and ActionChains
            self.wait = WebDriverWait(self.driver, 30)
            self.actions = ActionChains(self.driver)
            
            logger.info("Enhanced WebDriver setup completed")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to setup enhanced WebDriver: {e}")
            raise e
    
    def smart_element_finder(self, selectors: list, timeout: int = 10) -> Optional[any]:
        """Smart element finder with multiple selector strategies"""
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                elif selector.startswith("#"):
                    # ID selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.ID, selector[1:]))
                    )
                elif selector.startswith("."):
                    # Class selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.CLASS_NAME, selector[1:]))
                    )
                else:
                    # CSS selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                
                if element and element.is_displayed():
                    return element
                    
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
                continue
        
        logger.warning(f"No element found with selectors: {selectors}")
        return None
    
    def human_like_typing(self, element, text: str, typing_speed: float = 0.1) -> bool:
        """Type text with human-like delays"""
        try:
            element.clear()
            time.sleep(0.5)
            
            for char in text:
                element.send_keys(char)
                time.sleep(typing_speed + (0.05 * (0.5 - 0.5)))  # Random delay
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False
    
    def smart_click(self, element) -> bool:
        """Smart click with multiple strategies"""
        try:
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Try regular click
            try:
                element.click()
                return True
            except:
                pass
            
            # Try JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                pass
            
            # Try ActionChains click
            try:
                self.actions.move_to_element(element).click().perform()
                return True
            except:
                pass
            
            logger.warning("All click strategies failed")
            return False
            
        except Exception as e:
            logger.error(f"Smart click failed: {e}")
            return False
    
    def store_and_retrieve_user_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store user data and retrieve any existing data"""
        try:
            mobile = form_data.get('mobile')
            email = form_data.get('email')
            
            if not mobile:
                return form_data
            
            # Try to find existing user data
            existing_data = user_data_service.find_user_by_mobile(mobile)
            
            if existing_data:
                # Merge existing data with new data (new data takes precedence)
                merged_data = existing_data["form_data"].copy()
                merged_data.update(form_data)
                
                # Update stored data
                user_data_service.update_user_data(existing_data["user_key"], merged_data)
                self.current_user_key = existing_data["user_key"]
                
                logger.info(f"Retrieved and updated existing user data for mobile: {mobile}")
                return merged_data
            else:
                # Store new user data
                self.current_user_key = user_data_service.store_user_data(mobile, form_data, email)
                logger.info(f"Stored new user data for mobile: {mobile}")
                return form_data
                
        except Exception as e:
            logger.error(f"Failed to handle user data: {e}")
            return form_data
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None

    # GAS SERVICES - DIRECT ACCESS
    
    def submit_gujarat_gas_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gujarat Gas - Customer service form (Direct access)"""
        try:
            logger.info(f"Starting Gujarat Gas name change for consumer: {data.get('consumer_number')}")
            
            # Use headless mode for EC2
            self.setup_driver(headless=True, stealth_mode=True)
            
            # Navigate to the correct iConnect portal URL
            url = "https://iconnect.gujaratgas.com/Portal/outer-service-request_template.aspx"
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page load
            time.sleep(5)
            
            # Take initial screenshot
            initial_screenshot = f"screenshots/gujarat_gas_initial_{int(time.time())}.png"
            self.driver.save_screenshot(initial_screenshot)
            logger.info(f"Initial screenshot saved: {initial_screenshot}")
            
            # Check if page loaded correctly
            page_title = self.driver.title
            current_url = self.driver.current_url
            logger.info(f"Page loaded - Title: {page_title}, URL: {current_url}")
            
            # Try to find and fill form fields with multiple selector strategies
            form_filled = False
            
            try:
                # Look for consumer number field with multiple selectors
                consumer_selectors = [
                    "input[name='txtConsumerNo']",
                    "input[name='consumer_no']",
                    "input[name='consumerNumber']",
                    "input[id*='consumer']",
                    "input[placeholder*='consumer']",
                    "input[placeholder*='Consumer']"
                ]
                
                consumer_field = self.smart_element_finder(consumer_selectors, timeout=10)
                if consumer_field:
                    self.human_like_typing(consumer_field, data.get('consumer_number', ''))
                    logger.info("✅ Consumer number filled")
                    form_filled = True
                else:
                    logger.warning("❌ Consumer number field not found")
                
                # Fill current name
                current_name_selectors = [
                    "input[name='txtCurrentName']",
                    "input[name='current_name']",
                    "input[name='oldName']",
                    "input[id*='current']",
                    "input[placeholder*='current']"
                ]
                
                current_name_field = self.smart_element_finder(current_name_selectors, timeout=5)
                if current_name_field:
                    self.human_like_typing(current_name_field, data.get('old_name', ''))
                    logger.info("✅ Current name filled")
                    form_filled = True
                
                # Fill new name
                new_name_selectors = [
                    "input[name='txtNewName']",
                    "input[name='new_name']",
                    "input[name='newName']",
                    "input[id*='new']",
                    "input[placeholder*='new']"
                ]
                
                new_name_field = self.smart_element_finder(new_name_selectors, timeout=5)
                if new_name_field:
                    self.human_like_typing(new_name_field, data.get('new_name', ''))
                    logger.info("✅ New name filled")
                    form_filled = True
                
                # Fill mobile
                mobile_selectors = [
                    "input[name='txtMobile']",
                    "input[name='mobile']",
                    "input[type='tel']",
                    "input[id*='mobile']",
                    "input[placeholder*='mobile']"
                ]
                
                mobile_field = self.smart_element_finder(mobile_selectors, timeout=5)
                if mobile_field:
                    self.human_like_typing(mobile_field, data.get('mobile', ''))
                    logger.info("✅ Mobile filled")
                    form_filled = True
                
                # Fill email if provided
                if data.get('email'):
                    email_selectors = [
                        "input[name='txtEmail']",
                        "input[name='email']",
                        "input[type='email']",
                        "input[id*='email']"
                    ]
                    
                    email_field = self.smart_element_finder(email_selectors, timeout=5)
                    if email_field:
                        self.human_like_typing(email_field, data['email'])
                        logger.info("✅ Email filled")
                        form_filled = True
                
                # Fill address
                address_selectors = [
                    "textarea[name='txtAddress']",
                    "textarea[name='address']",
                    "input[name='address']",
                    "textarea[id*='address']"
                ]
                
                address_field = self.smart_element_finder(address_selectors, timeout=5)
                if address_field:
                    self.human_like_typing(address_field, data.get('address', ''))
                    logger.info("✅ Address filled")
                    form_filled = True
                
            except Exception as field_error:
                logger.warning(f"Form filling error: {field_error}")
            
            # Take final screenshot
            final_screenshot = f"screenshots/gujarat_gas_filled_{int(time.time())}.png"
            self.driver.save_screenshot(final_screenshot)
            logger.info(f"Final screenshot saved: {final_screenshot}")
            
            if form_filled:
                success_message = "Gujarat Gas form accessed and partially filled. Manual review and submission required."
                logger.info("✅ " + success_message)
            else:
                success_message = "Gujarat Gas website accessed but form fields not found. Manual form filling required."
                logger.warning("⚠️ " + success_message)
            
            return {
                "success": True,
                "message": success_message,
                "screenshot_path": final_screenshot,
                "website": "Gujarat Gas",
                "service": "Name Change",
                "form_filled": form_filled,
                "page_title": page_title,
                "current_url": current_url,
                "filled_data": data,
                "next_steps": [
                    "Review the website in the screenshot",
                    "Manually fill any missing fields",
                    "Submit the form after verification",
                    "Save confirmation number"
                ]
            }
            
        except Exception as e:
            logger.error(f"Gujarat Gas automation failed: {str(e)}")
            
            # Take error screenshot
            error_screenshot = None
            try:
                error_screenshot = f"screenshots/gujarat_gas_error_{int(time.time())}.png"
                if self.driver:
                    self.driver.save_screenshot(error_screenshot)
            except:
                pass
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Gujarat Gas automation failed: {str(e)}",
                "screenshot_path": error_screenshot,
                "website": "Gujarat Gas",
                "service": "Name Change"
            }
        finally:
            # Keep browser open for manual verification in non-headless mode
            # In headless mode, close the driver
            if self.driver:
                try:
                    if self.driver.execute_script("return navigator.webdriver") is None:
                        # Headless mode - close driver
                        self.close_driver()
                except:
                    # Close driver on any error
                    self.close_driver()
    
    def submit_vadodara_gas_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Vadodara Gas - Direct name change form (No login required)"""
        try:
            logger.info(f"Starting Vadodara Gas name change for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Direct URL to name change form
            url = "https://www.vgl.co.in/name-change-form"
            self.driver.get(url)
            
            # Wait for form to load
            self.wait.until(EC.presence_of_element_located((By.NAME, "consumer_number")))
            
            # Fill form fields
            if data.get('consumer_number'):
                consumer_field = self.driver.find_element(By.NAME, "consumer_number")
                consumer_field.clear()
                consumer_field.send_keys(data['consumer_number'])
                time.sleep(0.5)
            
            if data.get('old_name'):
                old_name_field = self.driver.find_element(By.NAME, "current_name")
                old_name_field.clear()
                old_name_field.send_keys(data['old_name'])
                time.sleep(0.5)
            
            if data.get('new_name'):
                new_name_field = self.driver.find_element(By.NAME, "new_name")
                new_name_field.clear()
                new_name_field.send_keys(data['new_name'])
                time.sleep(0.5)
            
            if data.get('mobile'):
                mobile_field = self.driver.find_element(By.NAME, "mobile")
                mobile_field.clear()
                mobile_field.send_keys(data['mobile'])
                time.sleep(0.5)
            
            # Take screenshot
            screenshot_path = f"screenshots/vadodara_gas_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "Vadodara Gas form filled successfully",
                "screenshot_path": screenshot_path,
                "website": "Vadodara Gas",
                "filled_data": data
            }
            
        except Exception as e:
            logger.error(f"Vadodara Gas automation failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    # ELECTRICITY SERVICES - DIRECT ACCESS
    
    def submit_torrent_power_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Torrent Power - Complete RPA automation with login and form filling"""
        try:
            logger.info(f"Starting Torrent Power RPA automation for service: {data.get('service_number')}")
            
            # Prepare login data
            login_data = {
                "username": data.get('username') or data.get('service_number'),
                "password": data.get('password', '')
            }
            
            # Prepare form data
            form_data = {
                "city": data.get('city', 'Ahmedabad'),
                "service_number": data.get('service_number'),
                "mobile": data.get('mobile'),
                "email": data.get('email'),
                "old_name": data.get('old_name'),
                "new_name": data.get('new_name')
            }
            
            # Use the dedicated Torrent Power service
            result = torrent_power_service.automate_name_change(login_data, form_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Torrent Power RPA automation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Torrent Power automation failed: {str(e)}",
                "website": "Torrent Power",
                "service": "Name Change"
            }
    
    # WATER SERVICES - DIRECT ACCESS
    
    def submit_gwssb_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """GWSSB - Direct forms page (No login required)"""
        try:
            logger.info(f"Starting GWSSB name change for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Direct URL to forms page
            url = "https://watersupply.gujarat.gov.in/forms"
            self.driver.get(url)
            
            # Wait for forms page
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "form-container")))
            
            # Look for name change form
            name_change_form = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Name Change")
            name_change_form.click()
            
            # Fill form if available
            time.sleep(2)
            
            # Try to fill basic fields
            try:
                if data.get('consumer_number'):
                    consumer_field = self.driver.find_element(By.NAME, "consumer_id")
                    consumer_field.send_keys(data['consumer_number'])
                
                if data.get('old_name'):
                    old_name_field = self.driver.find_element(By.NAME, "current_name")
                    old_name_field.send_keys(data['old_name'])
                
                if data.get('new_name'):
                    new_name_field = self.driver.find_element(By.NAME, "new_name")
                    new_name_field.send_keys(data['new_name'])
                
                if data.get('mobile'):
                    mobile_field = self.driver.find_element(By.NAME, "mobile")
                    mobile_field.send_keys(data['mobile'])
                    
            except Exception as field_error:
                logger.warning(f"Could not fill some fields: {field_error}")
            
            screenshot_path = f"screenshots/gwssb_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "GWSSB form accessed and filled",
                "screenshot_path": screenshot_path,
                "website": "GWSSB"
            }
            
        except Exception as e:
            logger.error(f"GWSSB automation failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    # PROPERTY SERVICES - DIRECT ACCESS
    
    def submit_anyror_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """AnyROR - Public record view & forms (No login required)"""
        try:
            logger.info(f"Starting AnyROR name change for property: {data.get('property_id')}")
            
            self.setup_driver(headless=True, stealth_mode=True)
            
            # Direct URL to public records
            url = "https://anyror.gujarat.gov.in"
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page load
            time.sleep(5)
            
            # Take initial screenshot
            initial_screenshot = f"screenshots/anyror_initial_{int(time.time())}.png"
            self.driver.save_screenshot(initial_screenshot)
            
            page_title = self.driver.title
            current_url = self.driver.current_url
            logger.info(f"AnyROR loaded - Title: {page_title}, URL: {current_url}")
            
            form_filled = False
            
            try:
                # Look for district dropdown
                district_selectors = [
                    "select[id='district']",
                    "select[name='district']",
                    "select[id*='district']"
                ]
                
                district_field = self.smart_element_finder(district_selectors, timeout=10)
                if district_field and data.get('district'):
                    from selenium.webdriver.support.ui import Select
                    district_select = Select(district_field)
                    district_select.select_by_visible_text(data['district'])
                    logger.info("✅ District selected")
                    form_filled = True
                    time.sleep(1)
                
                # Fill survey number
                survey_selectors = [
                    "input[id='survey_no']",
                    "input[name='survey_no']",
                    "input[name='surveyNumber']",
                    "input[id*='survey']"
                ]
                
                survey_field = self.smart_element_finder(survey_selectors, timeout=5)
                if survey_field and data.get('survey_number'):
                    self.human_like_typing(survey_field, data['survey_number'])
                    logger.info("✅ Survey number filled")
                    form_filled = True
                
                # Look for search button
                search_selectors = [
                    "button[id='search_btn']",
                    "input[type='submit']",
                    "button[type='submit']",
                    "button[id*='search']"
                ]
                
                search_btn = self.smart_element_finder(search_selectors, timeout=5)
                if search_btn:
                    self.smart_click(search_btn)
                    logger.info("✅ Search button clicked")
                    time.sleep(3)
                    form_filled = True
                
            except Exception as field_error:
                logger.warning(f"AnyROR form filling error: {field_error}")
            
            # Take final screenshot
            final_screenshot = f"screenshots/anyror_{int(time.time())}.png"
            self.driver.save_screenshot(final_screenshot)
            
            if form_filled:
                success_message = "AnyROR record search completed. Manual mutation process required for name change."
            else:
                success_message = "AnyROR website accessed but form fields not found. Manual search required."
            
            return {
                "success": True,
                "message": success_message,
                "screenshot_path": final_screenshot,
                "website": "AnyROR",
                "service": "Property Record Search",
                "form_filled": form_filled,
                "page_title": page_title,
                "current_url": current_url,
                "note": "For name change, visit e-Dhara center or Talati office with required documents.",
                "next_steps": [
                    "Review the property record in screenshot",
                    "Visit e-Dhara center or Talati office for name change",
                    "Carry required documents (sale deed, identity proof, etc.)",
                    "Complete mutation process manually"
                ]
            }
            
        except Exception as e:
            logger.error(f"AnyROR automation failed: {str(e)}")
            
            error_screenshot = None
            try:
                error_screenshot = f"screenshots/anyror_error_{int(time.time())}.png"
                if self.driver:
                    self.driver.save_screenshot(error_screenshot)
            except:
                pass
            
            return {
                "success": False,
                "error": str(e),
                "message": f"AnyROR automation failed: {str(e)}",
                "screenshot_path": error_screenshot,
                "website": "AnyROR"
            }
        finally:
            if self.driver:
                self.close_driver()

# Global enhanced service instance
direct_automation_service = EnhancedDirectAutomationService()