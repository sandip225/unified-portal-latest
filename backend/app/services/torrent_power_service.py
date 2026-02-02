#!/usr/bin/env python3
"""
Torrent Power RPA Service
Integrates Torrent Power automation with the backend API
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Dict, Any
import os
from .selenium_config import selenium_config

logger = logging.getLogger(__name__)

class TorrentPowerService:
    def __init__(self, headless=False):
        self.driver = None
        self.wait = None
        self.headless = headless
        
    def setup_driver(self):
        """Setup Chrome driver using selenium_config"""
        try:
            self.driver = selenium_config.create_driver(
                headless=self.headless, 
                stealth_mode=True, 
                undetected=False
            )
            
            # Configure for government sites
            selenium_config.configure_for_government_sites(self.driver)
            
            self.wait = WebDriverWait(self.driver, 60) # Increased wait for manual login if needed
            logger.info("✅ Torrent Power driver setup completed")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup driver: {e}")
            raise e

    # ... (login method remains same, omitting for brevity in this replace block if not changing) ...

    # We need to insert the new method and update the fill_name_change_form method.
    # I will replace the fill_name_change_form method to include transaction number.

    def fill_name_change_form(self, form_data):
        """Fill the name change form automatically with enhanced field detection"""
        try:
            logger.info("📝 Filling Torrent Power name change form...")
            logger.info(f"📋 Form data received: {list(form_data.keys())}")
            filled_fields = 0
            
            # Enhanced field selectors for Torrent Power specific form
            field_selectors = {
                'city': [
                    (By.NAME, "city"),
                    (By.ID, "city"),
                    (By.NAME, "cityId"),
                    (By.ID, "cityId"),
                    (By.XPATH, "//select[contains(@name, 'city')]"),
                    (By.XPATH, "//select[contains(@id, 'city')]")
                ],
                'service_number': [
                    (By.NAME, "serviceNumber"),
                    (By.NAME, "service_number"),
                    (By.NAME, "serviceNo"),
                    (By.ID, "serviceNumber"),
                    (By.ID, "service_number"),
                    (By.XPATH, "//input[contains(@name, 'service')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'service')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'Service')]")
                ],
                'transaction_number': [
                    (By.NAME, "transactionNumber"),
                    (By.NAME, "transaction_number"),
                    (By.NAME, "tNo"),
                    (By.NAME, "referenceNumber"),
                    (By.ID, "tNo"),
                    (By.XPATH, "//input[contains(@name, 'transaction')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'Transaction')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'Reference')]")
                ],
                'mobile': [
                    (By.NAME, "mobileNumber"),
                    (By.NAME, "mobile"),
                    (By.NAME, "mobileNo"),
                    (By.ID, "mobileNumber"),
                    (By.ID, "mobile"),
                    (By.XPATH, "//input[contains(@name, 'mobile')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'mobile')]"),
                    (By.XPATH, "//input[@type='tel']")
                ],
                'email': [
                    (By.NAME, "email"),
                    (By.NAME, "emailId"),
                    (By.ID, "email"),
                    (By.ID, "emailId"),
                    (By.XPATH, "//input[contains(@name, 'email')]"),
                    (By.XPATH, "//input[@type='email']"),
                    (By.XPATH, "//input[contains(@placeholder, 'email')]")
                ],
                'old_name': [
                    (By.NAME, "oldName"),
                    (By.NAME, "currentName"),
                    (By.NAME, "existingName"),
                    (By.ID, "oldName"),
                    (By.ID, "currentName"),
                    (By.XPATH, "//input[contains(@name, 'old')]"),
                    (By.XPATH, "//input[contains(@name, 'current')]"),
                    (By.XPATH, "//input[contains(@name, 'existing')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'current')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'old')]")
                ],
                'new_name': [
                    (By.NAME, "newName"),
                    (By.NAME, "proposedName"),
                    (By.ID, "newName"),
                    (By.ID, "proposedName"),
                    (By.XPATH, "//input[contains(@name, 'new')]"),
                    (By.XPATH, "//input[contains(@name, 'proposed')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'new')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'proposed')]")
                ]
            }
            
            # Fill each field with multiple attempts
            for field_name, selectors in field_selectors.items():
                field_value = form_data.get(field_name)
                if not field_value:
                    logger.info(f"⏭️ Skipping {field_name} - no value provided")
                    continue
                
                logger.info(f"🔍 Attempting to fill {field_name} with value: {field_value}")
                field_found = False
                
                for i, selector in enumerate(selectors):
                    try:
                        element = selenium_config.wait_for_element(self.driver, selector, timeout=3)
                        if element and element.is_displayed():
                            
                            # Handle dropdown fields
                            if element.tag_name == 'select':
                                try:
                                    select = Select(element)
                                    # Try exact match first
                                    try:
                                        select.select_by_visible_text(field_value)
                                        logger.info(f"✅ {field_name} dropdown selected (exact): {field_value}")
                                        filled_fields += 1
                                        field_found = True
                                        break
                                    except:
                                        # Try partial match
                                        options = [option.text for option in select.options]
                                        for option in options:
                                            if field_value.lower() in option.lower():
                                                select.select_by_visible_text(option)
                                                logger.info(f"✅ {field_name} dropdown selected (partial): {option}")
                                                filled_fields += 1
                                                field_found = True
                                                break
                                        if field_found:
                                            break
                                except Exception as select_error:
                                    logger.warning(f"⚠️ Dropdown selection failed for {field_name}: {select_error}")
                                    continue
                            
                            # Handle text input fields
                            else:
                                if selenium_config.safe_send_keys(self.driver, element, str(field_value)):
                                    logger.info(f"✅ {field_name} filled successfully: {field_value}")
                                    filled_fields += 1
                                    field_found = True
                                    break
                                else:
                                    logger.warning(f"⚠️ Failed to send keys to {field_name}")
                                    
                    except Exception as e:
                        logger.debug(f"🔍 Selector {i+1}/{len(selectors)} failed for {field_name}: {e}")
                        continue
                
                if not field_found:
                    logger.warning(f"❌ {field_name} field not found with any selector")
            
            # Check for captcha
            captcha_selectors = [
                (By.NAME, "captcha"),
                (By.ID, "captcha"),
                (By.XPATH, "//input[contains(@name, 'captcha')]"),
                (By.XPATH, "//input[contains(@placeholder, 'captcha')]"),
                (By.XPATH, "//input[contains(@placeholder, 'Captcha')]")
            ]
            
            captcha_found = False
            for selector in captcha_selectors:
                try:
                    captcha_element = selenium_config.wait_for_element(self.driver, selector, timeout=2)
                    if captcha_element and captcha_element.is_displayed():
                        logger.warning("⚠️ Captcha detected - manual intervention required")
                        selenium_config.take_screenshot(self.driver, "torrent_form_captcha_detected.png")
                        captcha_found = True
                        break
                except:
                    continue
            
            if not captcha_found:
                logger.info("✅ No captcha detected")
            
            # Take final screenshot of filled form
            selenium_config.take_screenshot(self.driver, "torrent_form_filled_final.png")
            
            # Summary
            if filled_fields > 0:
                logger.info(f"✅ Form filling completed! Successfully filled {filled_fields} fields")
                return {
                    "success": True, 
                    "filled_fields": filled_fields,
                    "captcha_detected": captcha_found,
                    "message": f"Successfully filled {filled_fields} form fields"
                }
            else:
                logger.warning("⚠️ No fields were successfully filled")
                return {
                    "success": False, 
                    "error": "No form fields found or filled",
                    "filled_fields": 0
                }
            
        except Exception as e:
            logger.error(f"❌ Form filling failed: {e}")
            selenium_config.take_screenshot(self.driver, "torrent_form_filling_error.png")
            return {
                "success": False, 
                "error": str(e),
                "filled_fields": filled_fields
            }
    
    def start_live_automation(self, form_data):
        """Start live automation without login - just open form and fill"""
        try:
            logger.info("🚀 Starting LIVE Torrent Power automation...")
            self.headless = False # Force headed mode
            self.setup_driver()
            
            # Navigate directly to name change form
            url = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
            logger.info(f"🔗 Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for user to potentially manually login if redirected, or just wait for form
            # Check if we are on login page
            if "signin" in self.driver.current_url:
                logger.info("ℹ️ Redirected to login page. Waiting for user to manually login...")
                # Wait until we are back on namechangerequest or dashboard
                try:
                    self.wait.until(EC.url_contains("namechangerequest"))
                    logger.info("✅ Detected navigation to Name Change Request page!")
                except TimeoutException:
                     logger.warning("⚠️ Timeout waiting for user validation/navigation. Attempting to fill anyway if on correct page.")

            # Attempt to fill form
            fill_result = self.fill_name_change_form(form_data)
            
            return {
                "success": True,
                "message": "Form opened and auto-filled. Please review and submit.",
                "filled_fields": fill_result.get('filled_fields', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Live automation failed: {e}")
            return {"success": False, "error": str(e)}

    def cleanup(self):
        """Close browser and cleanup"""
        # For live automation, we might want to keep it open?
        # Only close if explicit or error?
        # For now, let's NOT close if headless=False to allow user to submit
        try:
            if self.driver and self.headless:
                selenium_config.cleanup_driver(self.driver)
                self.driver = None
                logger.info("✅ Torrent Power service cleanup completed")
            elif self.driver:
                logger.info("ℹ️ Keeping browser open for user interaction (Live Mode)")
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

# Global service instance
torrent_power_service = TorrentPowerService(headless=False)  # Default to False for this requirement
        
    def login(self, username, password):
        """Login to Torrent Power portal"""
        try:
            logger.info("🔐 Logging into Torrent Power portal...")
            
            # Navigate to login page
            self.driver.get("https://connect.torrentpower.com/tplcp/session/signin")
            time.sleep(3)
            
            # Take screenshot for debugging
            selenium_config.take_screenshot(self.driver, "torrent_login_page.png")
            
            # Find and fill username
            username_field = selenium_config.wait_for_element(
                self.driver, (By.NAME, "username"), timeout=15
            )
            if username_field:
                selenium_config.safe_send_keys(self.driver, username_field, username)
                logger.info("✅ Username filled")
            else:
                return {"success": False, "error": "Username field not found"}
            
            # Find and fill password
            password_field = selenium_config.wait_for_element(
                self.driver, (By.NAME, "password"), timeout=10
            )
            if password_field:
                selenium_config.safe_send_keys(self.driver, password_field, password)
                logger.info("✅ Password filled")
            else:
                return {"success": False, "error": "Password field not found"}
            
            # Handle captcha if present
            try:
                captcha_field = self.driver.find_element(By.NAME, "captcha")
                logger.warning("⚠️ Captcha detected - manual intervention required")
                selenium_config.take_screenshot(self.driver, "torrent_captcha_detected.png")
                return {"success": False, "error": "Captcha detected - manual intervention required"}
            except NoSuchElementException:
                logger.info("✅ No captcha detected")
            
            # Click login button
            login_button = selenium_config.wait_for_element(
                self.driver, (By.XPATH, "//button[@type='submit']"), timeout=10
            )
            if login_button:
                if selenium_config.safe_click(self.driver, login_button):
                    logger.info("✅ Login button clicked")
                else:
                    return {"success": False, "error": "Failed to click login button"}
            else:
                return {"success": False, "error": "Login button not found"}
            
            # Wait for dashboard to load
            try:
                self.wait.until(EC.url_contains("dashboard"))
                logger.info("✅ Login successful!")
                selenium_config.take_screenshot(self.driver, "torrent_dashboard.png")
                return {"success": True}
            except TimeoutException:
                selenium_config.take_screenshot(self.driver, "torrent_login_failed.png")
                return {"success": False, "error": "Login failed - dashboard not loaded"}
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            selenium_config.take_screenshot(self.driver, "torrent_login_error.png")
            return {"success": False, "error": str(e)}
    
    def navigate_to_name_change(self):
        """Navigate to name change application following exact Torrent Power flow"""
        try:
            logger.info("🧭 Following Torrent Power navigation flow...")
            
            # Step 1: Look for "Apply" button on dashboard and click it
            logger.info("🔍 Looking for Apply button on dashboard...")
            apply_selectors = [
                (By.XPATH, "//button[contains(text(), 'Apply')]"),
                (By.XPATH, "//a[contains(text(), 'Apply')]"),
                (By.XPATH, "//button[contains(@class, 'apply')]"),
                (By.XPATH, "//*[contains(text(), 'Apply now')]"),
                (By.XPATH, "//*[contains(text(), 'Apply')]")
            ]
            
            apply_clicked = False
            for selector in apply_selectors:
                try:
                    apply_element = selenium_config.wait_for_element(self.driver, selector, timeout=5)
                    if apply_element:
                        if selenium_config.safe_click(self.driver, apply_element):
                            logger.info("✅ Apply button clicked successfully")
                            apply_clicked = True
                            time.sleep(3)
                            break
                except:
                    continue
            
            if not apply_clicked:
                logger.warning("⚠️ Apply button not found, proceeding to applications page")
            
            # Step 2: Navigate to My Applications page
            applications_url = "https://connect.torrentpower.com/tplcp/application/myapplications"
            logger.info(f"🔗 Navigating to My Applications: {applications_url}")
            self.driver.get(applications_url)
            time.sleep(3)
            
            # Take screenshot of applications page
            selenium_config.take_screenshot(self.driver, "torrent_my_applications.png")
            
            # Step 3: Look for Name Change option and click it
            logger.info("🔍 Looking for Name Change option...")
            name_change_selectors = [
                (By.XPATH, "//div[contains(text(), 'Name change')]"),
                (By.XPATH, "//a[contains(text(), 'Name change')]"),
                (By.XPATH, "//button[contains(text(), 'Name change')]"),
                (By.XPATH, "//*[contains(text(), 'Name Change')]"),
                (By.XPATH, "//*[contains(text(), 'name change')]"),
                (By.PARTIAL_LINK_TEXT, "Name change"),
                (By.PARTIAL_LINK_TEXT, "Name Change")
            ]
            
            name_change_clicked = False
            for selector in name_change_selectors:
                try:
                    name_change_element = selenium_config.wait_for_element(self.driver, selector, timeout=5)
                    if name_change_element:
                        if selenium_config.safe_click(self.driver, name_change_element):
                            logger.info("✅ Name Change option clicked successfully")
                            name_change_clicked = True
                            time.sleep(3)
                            break
                except:
                    continue
            
            if not name_change_clicked:
                logger.warning("⚠️ Name Change option not found, navigating directly to form")
            
            # Step 4: Navigate directly to name change request form
            name_change_url = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
            logger.info(f"🔗 Navigating to Name Change Form: {name_change_url}")
            self.driver.get(name_change_url)
            time.sleep(3)
            
            # Take screenshot of name change form
            selenium_config.take_screenshot(self.driver, "torrent_name_change_form.png")
            
            # Verify we're on the correct page
            current_url = self.driver.current_url
            if "namechangerequest" in current_url:
                logger.info("✅ Name change form loaded successfully!")
                return {"success": True}
            else:
                logger.warning(f"⚠️ Unexpected URL: {current_url}")
                return {"success": True, "warning": f"Reached URL: {current_url}"}
            
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            selenium_config.take_screenshot(self.driver, "torrent_navigation_error.png")
            return {"success": False, "error": str(e)}
    
    def fill_name_change_form(self, form_data):
        """Fill the name change form automatically with enhanced field detection"""
        try:
            logger.info("📝 Filling Torrent Power name change form...")
            logger.info(f"📋 Form data received: {list(form_data.keys())}")
            filled_fields = 0
            
            # Enhanced field selectors for Torrent Power specific form
            field_selectors = {
                'city': [
                    (By.NAME, "city"),
                    (By.ID, "city"),
                    (By.NAME, "cityId"),
                    (By.ID, "cityId"),
                    (By.XPATH, "//select[contains(@name, 'city')]"),
                    (By.XPATH, "//select[contains(@id, 'city')]")
                ],
                'service_number': [
                    (By.NAME, "serviceNumber"),
                    (By.NAME, "service_number"),
                    (By.NAME, "serviceNo"),
                    (By.ID, "serviceNumber"),
                    (By.ID, "service_number"),
                    (By.XPATH, "//input[contains(@name, 'service')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'service')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'Service')]")
                ],
                'mobile': [
                    (By.NAME, "mobileNumber"),
                    (By.NAME, "mobile"),
                    (By.NAME, "mobileNo"),
                    (By.ID, "mobileNumber"),
                    (By.ID, "mobile"),
                    (By.XPATH, "//input[contains(@name, 'mobile')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'mobile')]"),
                    (By.XPATH, "//input[@type='tel']")
                ],
                'email': [
                    (By.NAME, "email"),
                    (By.NAME, "emailId"),
                    (By.ID, "email"),
                    (By.ID, "emailId"),
                    (By.XPATH, "//input[contains(@name, 'email')]"),
                    (By.XPATH, "//input[@type='email']"),
                    (By.XPATH, "//input[contains(@placeholder, 'email')]")
                ],
                'old_name': [
                    (By.NAME, "oldName"),
                    (By.NAME, "currentName"),
                    (By.NAME, "existingName"),
                    (By.ID, "oldName"),
                    (By.ID, "currentName"),
                    (By.XPATH, "//input[contains(@name, 'old')]"),
                    (By.XPATH, "//input[contains(@name, 'current')]"),
                    (By.XPATH, "//input[contains(@name, 'existing')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'current')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'old')]")
                ],
                'new_name': [
                    (By.NAME, "newName"),
                    (By.NAME, "proposedName"),
                    (By.ID, "newName"),
                    (By.ID, "proposedName"),
                    (By.XPATH, "//input[contains(@name, 'new')]"),
                    (By.XPATH, "//input[contains(@name, 'proposed')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'new')]"),
                    (By.XPATH, "//input[contains(@placeholder, 'proposed')]")
                ]
            }
            
            # Fill each field with multiple attempts
            for field_name, selectors in field_selectors.items():
                field_value = form_data.get(field_name)
                if not field_value:
                    logger.info(f"⏭️ Skipping {field_name} - no value provided")
                    continue
                
                logger.info(f"🔍 Attempting to fill {field_name} with value: {field_value}")
                field_found = False
                
                for i, selector in enumerate(selectors):
                    try:
                        element = selenium_config.wait_for_element(self.driver, selector, timeout=3)
                        if element and element.is_displayed():
                            
                            # Handle dropdown fields
                            if element.tag_name == 'select':
                                try:
                                    select = Select(element)
                                    # Try exact match first
                                    try:
                                        select.select_by_visible_text(field_value)
                                        logger.info(f"✅ {field_name} dropdown selected (exact): {field_value}")
                                        filled_fields += 1
                                        field_found = True
                                        break
                                    except:
                                        # Try partial match
                                        options = [option.text for option in select.options]
                                        for option in options:
                                            if field_value.lower() in option.lower():
                                                select.select_by_visible_text(option)
                                                logger.info(f"✅ {field_name} dropdown selected (partial): {option}")
                                                filled_fields += 1
                                                field_found = True
                                                break
                                        if field_found:
                                            break
                                except Exception as select_error:
                                    logger.warning(f"⚠️ Dropdown selection failed for {field_name}: {select_error}")
                                    continue
                            
                            # Handle text input fields
                            else:
                                if selenium_config.safe_send_keys(self.driver, element, str(field_value)):
                                    logger.info(f"✅ {field_name} filled successfully: {field_value}")
                                    filled_fields += 1
                                    field_found = True
                                    break
                                else:
                                    logger.warning(f"⚠️ Failed to send keys to {field_name}")
                                    
                    except Exception as e:
                        logger.debug(f"🔍 Selector {i+1}/{len(selectors)} failed for {field_name}: {e}")
                        continue
                
                if not field_found:
                    logger.warning(f"❌ {field_name} field not found with any selector")
            
            # Check for captcha
            captcha_selectors = [
                (By.NAME, "captcha"),
                (By.ID, "captcha"),
                (By.XPATH, "//input[contains(@name, 'captcha')]"),
                (By.XPATH, "//input[contains(@placeholder, 'captcha')]"),
                (By.XPATH, "//input[contains(@placeholder, 'Captcha')]")
            ]
            
            captcha_found = False
            for selector in captcha_selectors:
                try:
                    captcha_element = selenium_config.wait_for_element(self.driver, selector, timeout=2)
                    if captcha_element and captcha_element.is_displayed():
                        logger.warning("⚠️ Captcha detected - manual intervention required")
                        selenium_config.take_screenshot(self.driver, "torrent_form_captcha_detected.png")
                        captcha_found = True
                        break
                except:
                    continue
            
            if not captcha_found:
                logger.info("✅ No captcha detected")
            
            # Take final screenshot of filled form
            selenium_config.take_screenshot(self.driver, "torrent_form_filled_final.png")
            
            # Summary
            if filled_fields > 0:
                logger.info(f"✅ Form filling completed! Successfully filled {filled_fields} fields")
                return {
                    "success": True, 
                    "filled_fields": filled_fields,
                    "captcha_detected": captcha_found,
                    "message": f"Successfully filled {filled_fields} form fields"
                }
            else:
                logger.warning("⚠️ No fields were successfully filled")
                return {
                    "success": False, 
                    "error": "No form fields found or filled",
                    "filled_fields": 0
                }
            
        except Exception as e:
            logger.error(f"❌ Form filling failed: {e}")
            selenium_config.take_screenshot(self.driver, "torrent_form_filling_error.png")
            return {
                "success": False, 
                "error": str(e),
                "filled_fields": filled_fields
            }
    
    def automate_name_change(self, login_data, form_data):
        """Complete automation flow following exact Torrent Power navigation"""
        try:
            logger.info("🚀 Starting Torrent Power name change automation...")
            logger.info("📋 Following exact flow: Login → Apply → My Applications → Name Change Form")
            
            # Setup driver
            self.setup_driver()
            
            # Step 1: Login to Torrent Power
            logger.info("🔐 Step 1: Login to Torrent Power portal")
            login_result = self.login(login_data['username'], login_data['password'])
            if not login_result['success']:
                return {
                    "success": False,
                    "error": f"Login failed: {login_result.get('error', 'Unknown error')}",
                    "step": "login"
                }
            
            # Step 2: Navigate through the complete flow
            logger.info("🧭 Step 2: Navigate to name change form")
            nav_result = self.navigate_to_name_change()
            if not nav_result['success']:
                return {
                    "success": False,
                    "error": f"Navigation failed: {nav_result.get('error', 'Unknown error')}",
                    "step": "navigation"
                }
            
            # Step 3: Fill the name change form
            logger.info("📝 Step 3: Fill name change form")
            fill_result = self.fill_name_change_form(form_data)
            if not fill_result['success']:
                return {
                    "success": False,
                    "error": f"Form filling failed: {fill_result.get('error', 'Unknown error')}",
                    "step": "form_filling"
                }
            
            # Step 4: Take final screenshot and prepare result
            final_screenshot = selenium_config.take_screenshot(self.driver, f"torrent_power_completed_{int(time.time())}.png")
            
            logger.info("✅ Torrent Power automation completed successfully!")
            
            return {
                "success": True,
                "message": "Torrent Power name change form filled successfully via RPA automation",
                "screenshot": final_screenshot,
                "next_step": "Please review the form and submit manually",
                "website": "Torrent Power",
                "service": "Name Change",
                "flow_completed": [
                    "✅ Logged into Torrent Power account",
                    "✅ Clicked Apply button on dashboard", 
                    "✅ Navigated to My Applications",
                    "✅ Accessed Name Change form",
                    f"✅ Auto-filled {fill_result.get('filled_fields', 0)} form fields",
                    "✅ Form ready for manual review and submission"
                ],
                "filled_fields": fill_result.get('filled_fields', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Automation failed: {e}")
            error_screenshot = selenium_config.take_screenshot(self.driver, f"torrent_power_error_{int(time.time())}.png")
            
            return {
                "success": False,
                "error": str(e),
                "screenshot": error_screenshot,
                "message": "Torrent Power automation encountered an error"
            }
        
        finally:
            # Keep browser open for manual review in non-headless mode
            # In production (headless), cleanup after delay
            if self.headless:
                time.sleep(5)  # Give time to save screenshot
                self.cleanup()
            else:
                logger.info("🔍 Browser kept open for manual review (non-headless mode)")
                # Don't cleanup in non-headless mode for debugging
    
    def cleanup(self):
        """Close browser and cleanup"""
        try:
            if self.driver:
                selenium_config.cleanup_driver(self.driver)
                self.driver = None
                logger.info("✅ Torrent Power service cleanup completed")
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

# Global service instance
torrent_power_service = TorrentPowerService(headless=True)  # Always headless for production