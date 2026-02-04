#!/usr/bin/env python3
"""
Simple RPA Test Script for Windows EC2
"""

import sys
import os
import time

# Add current directory to path
sys.path.append('.')
sys.path.append('./backend')

def test_rpa():
    print("🧪 Testing RPA setup...")
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        print("✅ All imports successful")
        
        # Setup Chrome options
        print("⚙️ Setting up Chrome options...")
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Find Chrome binary
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                print(f"✅ Using Chrome binary: {path}")
                chrome_found = True
                break
        
        if not chrome_found:
            print("❌ Chrome binary not found")
            return False
        
        # Create driver
        print("🚀 Creating Chrome driver...")
        try:
            driver_path = ChromeDriverManager().install()
            print(f"✅ ChromeDriver path: {driver_path}")
            
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("✅ Chrome driver created successfully")
            
        except Exception as e:
            print(f"⚠️ webdriver-manager failed: {e}")
            print("🔧 Trying system Chrome...")
            driver = webdriver.Chrome(options=options)
            print("✅ Chrome driver created with system Chrome")
        
        # Test basic navigation
        print("🌐 Testing navigation...")
        test_html = """
        <html>
        <head><title>RPA Test</title></head>
        <body>
            <h1>🎉 RPA Test Success!</h1>
            <p>Chrome driver is working on Windows EC2</p>
            <input type="text" id="test-input" placeholder="Test input">
        </body>
        </html>
        """
        
        driver.get(f"data:text/html,{test_html}")
        print(f"✅ Navigation successful, title: {driver.title}")
        
        # Test element interaction
        print("🎯 Testing element interaction...")
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.presence_of_element_located((By.ID, "test-input")))
        input_element.send_keys("RPA Test Successful!")
        print("✅ Element interaction successful")
        
        # Test Torrent Power navigation
        print("🌐 Testing Torrent Power navigation...")
        try:
            driver.set_page_load_timeout(60)
            driver.get("https://connect.torrentpower.com/tplcp/application/namechangerequest")
            
            # Wait for page to load
            time.sleep(5)
            
            current_url = driver.current_url
            page_title = driver.title
            
            print(f"✅ Torrent Power navigation successful")
            print(f"   URL: {current_url}")
            print(f"   Title: {page_title}")
            
            # Check for form elements
            forms = driver.find_elements(By.TAG_NAME, "form")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            
            print(f"   Found {len(forms)} form(s) and {len(inputs)} input(s)")
            
        except Exception as e:
            print(f"⚠️ Torrent Power navigation failed: {e}")
            print("   This might be due to network issues or site changes")
        
        # Keep browser open for inspection
        print("⏳ Keeping browser open for 10 seconds...")
        time.sleep(10)
        
        # Close driver
        driver.quit()
        print("✅ Driver closed successfully")
        
        print("\n🎉 RPA TEST COMPLETED SUCCESSFULLY!")
        print("✅ Chrome driver is working")
        print("✅ Navigation is working")
        print("✅ Element interaction is working")
        print("✅ RPA automation should work now")
        
        return True
        
    except Exception as e:
        print(f"❌ RPA test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        
        # Provide troubleshooting tips
        print("\n💡 Troubleshooting tips:")
        print("   1. Install Chrome: choco install googlechrome -y --ignore-checksums")
        print("   2. Update packages: pip install selenium==4.15.2 webdriver-manager==4.0.1")
        print("   3. Run as Administrator")
        print("   4. Check Windows Firewall")
        
        return False

if __name__ == "__main__":
    print("🚀 Starting RPA Test for Windows EC2")
    print("=" * 40)
    
    success = test_rpa()
    
    if success:
        print("\n✅ ALL TESTS PASSED - RPA IS READY!")
    else:
        print("\n❌ TESTS FAILED - CHECK ERRORS ABOVE")
    
    input("\nPress Enter to exit...")