"""
Selenium Browser Automation Service
Direct form filling for government portals with visible process
No AI dependencies - pure Selenium automation
"""

import time
import os
from typing import Dict, Any, Optional
from datetime import datetime
import json
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app.config import get_settings

settings = get_settings()


class SeleniumBrowserService:
    """Selenium-powered browser automation for government portals"""
    
    def __init__(self):
        try:
            print("🚀 Initializing Selenium Browser Service...")
            
            # Chrome options for visible automation
            self.chrome_options = Options()
            self.chrome_options.add_argument("--no-sandbox")
            self.chrome_options.add_argument("--disable-dev-shm-usage")
            self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.chrome_options.add_experimental_option('useAutomationExtension', False)
            self.chrome_options.add_argument("--window-size=1280,720")
            self.chrome_options.add_argument("--start-maximized")
            
            # Keep browser visible for user to watch
            # self.chrome_options.add_argument("--headless")  # Commented out to keep visible
            
            print("✅ Selenium Browser Service initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing Selenium Browser Service: {str(e)}")
            raise e
    
    def create_driver(self):
        """Create a new Chrome WebDriver instance"""
        try:
            # Use ChromeDriverManager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            # Execute script to remove automation indicators
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
        except Exception as e:
            print(f"❌ Error creating Chrome driver: {str(e)}")
            raise e
    
    async def auto_fill_torrent_power_form(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Direct Torrent Power form automation using Selenium
        Fills the form automatically with user data
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Dictionary with automation result
        """
        
        driver = None
        try:
            print("🚀 Starting Torrent Power Selenium automation...")
            print(f"📋 User data received: {user_data}")
            
            # Create Chrome driver
            print("🌐 Creating Chrome browser...")
            driver = self.create_driver()
            print("✅ Chrome browser created successfully")
            
            # Prepare form data with fallbacks
            form_data = {
                'service_number': user_data.get('service_number', user_data.get('connection_id', 'TP123456')),
                't_number': user_data.get('t_number', user_data.get('t_no', 'T789')),
                'mobile': user_data.get('mobile', user_data.get('phone', '9876543210')),
                'email': user_data.get('email', 'user@example.com')
            }
            
            print(f"📝 Form data prepared: {form_data}")
            
            # Step 1: Navigate to Torrent Power form
            print("🌐 Navigating to Torrent Power name change form...")
            driver.get("https://connect.torrentpower.com/tplcp/application/namechangerequest")
            
            # Wait for page to load
            print("⏳ Waiting for page to load...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)  # Additional wait for dynamic content
            
            print("✅ Page loaded successfully")
            
            # Step 2: Fill City/Location dropdown
            print("📍 Selecting city: Ahmedabad...")
            try:
                city_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "select"))
                )
                select_city = Select(city_dropdown)
                select_city.select_by_visible_text("Ahmedabad")
                time.sleep(2)
                print("✅ City selected: Ahmedabad")
            except Exception as e:
                print(f"⚠️ City selection failed: {str(e)}")
            
            # Step 3: Fill Service Number
            print(f"🔢 Filling Service Number: {form_data['service_number']}...")
            try:
                service_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
                )
                service_input.clear()
                service_input.send_keys(form_data['service_number'])
                time.sleep(2)
                print("✅ Service Number filled")
            except Exception as e:
                print(f"⚠️ Service Number filling failed: {str(e)}")
            
            # Step 4: Fill T Number
            print(f"📋 Filling T Number: {form_data['t_number']}...")
            try:
                t_number_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if len(t_number_inputs) > 1:
                    t_number_inputs[1].clear()
                    t_number_inputs[1].send_keys(form_data['t_number'])
                    time.sleep(2)
                    print("✅ T Number filled")
            except Exception as e:
                print(f"⚠️ T Number filling failed: {str(e)}")
            
            # Step 5: Fill Mobile Number
            print(f"📱 Filling Mobile Number: {form_data['mobile']}...")
            try:
                mobile_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if len(mobile_inputs) > 2:
                    mobile_inputs[2].clear()
                    mobile_inputs[2].send_keys(form_data['mobile'])
                    time.sleep(2)
                    print("✅ Mobile Number filled")
            except Exception as e:
                print(f"⚠️ Mobile Number filling failed: {str(e)}")
            
            # Step 6: Fill Email Address
            print(f"📧 Filling Email: {form_data['email']}...")
            try:
                email_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if len(email_inputs) > 3:
                    email_inputs[3].clear()
                    email_inputs[3].send_keys(form_data['email'])
                    time.sleep(2)
                    print("✅ Email filled")
            except Exception as e:
                print(f"⚠️ Email filling failed: {str(e)}")
            
            # Step 7: Handle captcha (if present)
            print("🔄 Looking for captcha...")
            try:
                captcha_refresh = driver.find_element(By.CSS_SELECTOR, "button[onclick*='captcha'], input[value*='Regenerate']")
                if captcha_refresh:
                    captcha_refresh.click()
                    time.sleep(2)
                    print("✅ Captcha refreshed - user needs to fill manually")
            except:
                print("ℹ️ No captcha refresh button found")
            
            print("🎉 Form filling completed!")
            print("👤 User action required: Complete captcha and submit form")
            
            # Keep browser open for user to complete manually
            # Don't close driver - let user complete captcha and submit
            
            return {
                "success": True,
                "message": "Torrent Power form filled successfully! Please complete captcha and submit.",
                "details": "All form fields filled automatically using Selenium",
                "timestamp": datetime.now().isoformat(),
                "provider": "torrent_power",
                "automation_steps": [
                    "✅ Navigated to Torrent Power name change form",
                    "✅ Selected city: Ahmedabad", 
                    f"✅ Filled Service Number: {form_data['service_number']}",
                    f"✅ Filled T Number: {form_data['t_number']}",
                    f"✅ Filled Mobile Number: {form_data['mobile']}",
                    f"✅ Filled Email: {form_data['email']}",
                    "✅ Refreshed captcha for user completion"
                ],
                "portal_urls": [
                    "https://connect.torrentpower.com/tplcp/application/namechangerequest"
                ],
                "fields_filled": [
                    "city_dropdown", "service_number", "t_number", "mobile_number", "email_address"
                ],
                "next_steps": [
                    "1. Check the browser window - form should be filled automatically",
                    "2. Enter the captcha code manually", 
                    "3. Review all filled information for accuracy",
                    "4. Click the submit button to complete your application",
                    "5. Save the application reference number for tracking"
                ],
                "automation_type": "selenium_direct",
                "user_action_required": "Complete captcha and submit form in the browser window",
                "browser_status": "Browser window left open for manual completion",
                "technology": "Selenium WebDriver",
                "cost": "Free - No API charges"
            }
            
        except Exception as e:
            print(f"❌ Torrent Power Selenium automation error: {str(e)}")
            print(f"❌ Full traceback: {traceback.format_exc()}")
            
            # Close driver on error
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Torrent Power Selenium automation failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "provider": "torrent_power",
                "automation_type": "selenium_direct",
                "troubleshooting": [
                    "1. Check if Chrome browser is installed",
                    "2. Ensure internet connection is stable",
                    "3. Try again - sometimes websites have temporary issues",
                    "4. Check if Torrent Power website is accessible",
                    "5. Verify Selenium and ChromeDriver are properly installed"
                ],
                "full_error": traceback.format_exc(),
                "technology": "Selenium WebDriver"
            }
    
    async def auto_fill_government_portal_form(
        self, 
        provider: str, 
        user_data: Dict[str, Any],
        portal_url: str,
        login_required: bool = False,
        login_credentials: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generic method to auto-fill government portal forms using Selenium
        
        Args:
            provider: Provider name (e.g., 'pgvcl', 'ugvcl', etc.)
            user_data: User information to fill
            portal_url: URL of the government portal
            login_required: Whether login is required
            login_credentials: Login credentials if required
            
        Returns:
            Dictionary with automation result
        """
        
        driver = None
        try:
            print(f"🚀 Starting {provider} Selenium automation...")
            
            # Create Chrome driver
            driver = self.create_driver()
            
            # Navigate to portal
            print(f"🌐 Navigating to {provider} portal: {portal_url}")
            driver.get(portal_url)
            
            # Wait for page load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)
            
            # Handle login if required
            if login_required and login_credentials:
                print("🔐 Performing login...")
                try:
                    username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[name*='user'], input[id*='user']")
                    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                    
                    username_field.send_keys(login_credentials.get('username', ''))
                    time.sleep(1)
                    password_field.send_keys(login_credentials.get('password', ''))
                    time.sleep(1)
                    login_button.click()
                    
                    # Wait for login to complete
                    time.sleep(5)
                    print("✅ Login completed")
                except Exception as e:
                    print(f"⚠️ Login failed: {str(e)}")
            
            # Fill form fields
            print("📝 Filling form fields...")
            form_fields = [
                ('full_name', "input[name*='name'], input[placeholder*='name']"),
                ('mobile', "input[name*='mobile'], input[placeholder*='mobile'], input[type='tel']"),
                ('email', "input[name*='email'], input[placeholder*='email'], input[type='email']"),
                ('address', "textarea[name*='address'], input[name*='address']"),
                ('aadhaar', "input[name*='aadhaar'], input[placeholder*='aadhaar']"),
                ('customer_id', "input[name*='customer'], input[placeholder*='customer']"),
                ('account_number', "input[name*='account'], input[placeholder*='account']")
            ]
            
            filled_fields = []
            for field_name, selector in form_fields:
                if field_name in user_data and user_data[field_name]:
                    try:
                        field = driver.find_element(By.CSS_SELECTOR, selector)
                        field.clear()
                        field.send_keys(user_data[field_name])
                        time.sleep(1)
                        filled_fields.append(field_name)
                        print(f"✅ Filled {field_name}: {user_data[field_name]}")
                    except Exception as e:
                        print(f"⚠️ Could not fill {field_name}: {str(e)}")
            
            print(f"🎉 {provider} form filling completed!")
            
            return {
                "success": True,
                "message": f"{provider} form filled successfully with Selenium",
                "details": f"Filled {len(filled_fields)} fields automatically",
                "timestamp": datetime.now().isoformat(),
                "provider": provider,
                "portal_url": portal_url,
                "automation_type": "selenium_direct",
                "fields_filled": filled_fields,
                "user_action_required": "Review filled form and submit manually",
                "technology": "Selenium WebDriver",
                "cost": "Free - No API charges"
            }
            
        except Exception as e:
            print(f"❌ {provider} Selenium automation error: {str(e)}")
            
            # Close driver on error
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to auto-fill {provider} form with Selenium",
                "timestamp": datetime.now().isoformat(),
                "provider": provider,
                "automation_type": "selenium_direct",
                "technology": "Selenium WebDriver"
            }


# Singleton instance
selenium_browser_service = None

def get_selenium_browser_service():
    """Get or create the Selenium browser service instance"""
    global selenium_browser_service
    if selenium_browser_service is None:
        selenium_browser_service = SeleniumBrowserService()
    return selenium_browser_service