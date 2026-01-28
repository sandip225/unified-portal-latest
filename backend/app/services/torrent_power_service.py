#!/usr/bin/env python3
"""
Torrent Power RPA Service
Integrates Torrent Power automation with the backend API
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)

class TorrentPowerService:
    def __init__(self, headless=True):
        self.driver = None
        self.wait = None
        self.headless = headless
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
    def login(self, username, password):
        """Login to Torrent Power portal"""
        try:
            logger.info("🔐 Logging into Torrent Power portal...")
            
            # Navigate to login page
            self.driver.get("https://connect.torrentpower.com/tplcp/session/signin")
            time.sleep(3)
            
            # Find and fill username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(username)
            
            # Find and fill password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Handle captcha if present
            try:
                captcha_field = self.driver.find_element(By.NAME, "captcha")
                logger.warning("⚠️ Captcha detected - manual intervention required")
                return {"success": False, "error": "Captcha detected - manual intervention required"}
            except NoSuchElementException:
                pass
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for dashboard to load
            self.wait.until(EC.url_contains("dashboard"))
            logger.info("✅ Login successful!")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            return {"success": False, "error": str(e)}
    
    def navigate_to_name_change(self):
        """Navigate to name change application"""
        try:
            logger.info("🧭 Navigating to name change application...")
            
            # Look for "Apply now" button on dashboard
            apply_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply now')]")
            if apply_buttons:
                apply_buttons[0].click()
                time.sleep(2)
            
            # Navigate to applications page
            self.driver.get("https://connect.torrentpower.com/tplcp/application/myapplications")
            time.sleep(3)
            
            # Click on "Name change" option
            name_change_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Name change')]"))
            )
            name_change_button.click()
            time.sleep(3)
            
            # Wait for name change form to load
            self.wait.until(EC.url_contains("namechangerequest"))
            logger.info("✅ Name change form loaded!")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def fill_name_change_form(self, form_data):
        """Fill the name change form automatically"""
        try:
            logger.info("📝 Filling name change form...")
            
            # Select city dropdown
            if form_data.get('city'):
                try:
                    city_dropdown = Select(self.driver.find_element(By.NAME, "city"))
                    city_dropdown.select_by_visible_text(form_data['city'])
                    time.sleep(1)
                except:
                    logger.warning("City dropdown not found or not selectable")
            
            # Fill service number
            if form_data.get('service_number'):
                try:
                    service_field = self.driver.find_element(By.NAME, "serviceNumber")
                    service_field.clear()
                    service_field.send_keys(form_data['service_number'])
                    time.sleep(1)
                except:
                    logger.warning("Service number field not found")
            
            # Fill mobile number
            if form_data.get('mobile'):
                try:
                    mobile_field = self.driver.find_element(By.NAME, "mobileNumber")
                    mobile_field.clear()
                    mobile_field.send_keys(form_data['mobile'])
                    time.sleep(1)
                except:
                    logger.warning("Mobile field not found")
            
            # Fill email
            if form_data.get('email'):
                try:
                    email_field = self.driver.find_element(By.NAME, "email")
                    email_field.clear()
                    email_field.send_keys(form_data['email'])
                    time.sleep(1)
                except:
                    logger.warning("Email field not found")
            
            # Fill old name
            if form_data.get('old_name'):
                try:
                    old_name_field = self.driver.find_element(By.NAME, "oldName")
                    old_name_field.clear()
                    old_name_field.send_keys(form_data['old_name'])
                    time.sleep(1)
                except:
                    logger.warning("Old name field not found")
            
            # Fill new name
            if form_data.get('new_name'):
                try:
                    new_name_field = self.driver.find_element(By.NAME, "newName")
                    new_name_field.clear()
                    new_name_field.send_keys(form_data['new_name'])
                    time.sleep(1)
                except:
                    logger.warning("New name field not found")
            
            # Handle captcha
            try:
                captcha_field = self.driver.find_element(By.NAME, "captcha")
                logger.warning("⚠️ Captcha detected - manual intervention required")
                return {"success": False, "error": "Captcha detected - manual intervention required"}
            except NoSuchElementException:
                pass
            
            logger.info("✅ Form filled successfully!")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"❌ Form filling failed: {e}")
            return {"success": False, "error": str(e)}
    
    def automate_name_change(self, login_data, form_data):
        """Complete automation flow"""
        try:
            logger.info("🚀 Starting Torrent Power name change automation...")
            
            # Setup driver
            self.setup_driver()
            
            # Step 1: Login
            login_result = self.login(login_data['username'], login_data['password'])
            if not login_result['success']:
                return login_result
            
            # Step 2: Navigate to name change
            nav_result = self.navigate_to_name_change()
            if not nav_result['success']:
                return nav_result
            
            # Step 3: Fill form
            fill_result = self.fill_name_change_form(form_data)
            if not fill_result['success']:
                return fill_result
            
            # Take screenshot for verification
            screenshot_path = f"screenshots/torrent_power_form_{int(time.time())}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "Torrent Power name change form filled successfully",
                "screenshot": screenshot_path,
                "next_step": "Manual review and submission recommended",
                "website": "Torrent Power",
                "service": "Name Change"
            }
            
        except Exception as e:
            logger.error(f"Automation failed: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            self.driver = None

# Global service instance
torrent_power_service = TorrentPowerService()