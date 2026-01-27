# Selenium Integration Guide for Unified Portal

## Overview

Your portal now has comprehensive Selenium automation capabilities that work seamlessly with your existing RPA system. This guide explains how to use and extend the Selenium integration.

## What is Selenium?

Selenium is a powerful web automation framework that programmatically controls web browsers. In your portal, it's used for:

- **Automated Form Filling**: Automatically fill government website forms
- **Cross-Browser Testing**: Test your portal across different browsers
- **Web Scraping**: Extract data from government websites
- **RPA (Robotic Process Automation)**: Automate repetitive tasks

## Current Implementation

### 1. Base RPA Service (`backend/app/services/rpa_service.py`)
Your existing RPA service already uses Selenium for:
- Torrent Power automation
- Adani Gas automation
- AMC Water automation
- AnyRoR Gujarat automation

### 2. Enhanced Selenium Service (`backend/app/services/enhanced_selenium_service.py`)
New advanced features:
- Smart form filling with human-like typing
- Full-page screenshots
- Mobile device emulation
- Form data extraction
- Automation reporting

### 3. Chrome Extension Integration (`chrome-extension/selenium-bridge.js`)
- Detects government websites automatically
- Extracts form data from current page
- Communicates with backend for automation
- Provides visual feedback to users

### 4. API Endpoints (`backend/app/routers/selenium_automation.py`)
- `/api/selenium/start-automation` - Start automation tasks
- `/api/selenium/task-status/{task_id}` - Monitor task progress
- `/api/selenium/extract-form-data` - Extract form data from URLs
- `/api/selenium/validate-site` - Check if site is supported
- `/api/selenium/supported-services` - List all supported services

## How to Use Selenium in Your Portal

### 1. Frontend Integration

Add the Selenium demo page to your app routing:

```jsx
// In your App.jsx or routing file
import SeleniumDemo from './pages/SeleniumDemo';

// Add to your routes
<Route path="/selenium-demo" element={<SeleniumDemo />} />
```

### 2. Chrome Extension Usage

The Chrome extension automatically:
1. Detects supported government websites
2. Shows automation control panel
3. Extracts form data
4. Communicates with your backend

To activate:
1. Install the Chrome extension
2. Visit a supported government website
3. Click the extension icon
4. Use the automation controls

### 3. API Usage Examples

#### Start Automation
```javascript
const response = await fetch('/api/selenium/start-automation', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    service_type: 'torrent_power',
    form_data: {
      city: 'Ahmedabad',
      service_number: 'TP2025123456',
      applicant_name: 'John Doe',
      mobile: '9876543210',
      email: 'john@example.com',
      application_type: 'name_change'
    },
    source: 'frontend'
  })
});
```

#### Monitor Task Progress
```javascript
const taskStatus = await fetch(`/api/selenium/task-status/${taskId}`);
const status = await taskStatus.json();
console.log(`Progress: ${status.progress}%`);
```

#### Extract Form Data
```javascript
const response = await fetch('/api/selenium/extract-form-data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://connect.torrentpower.com',
    options: { headless: true }
  })
});
```

## Supported Government Services

### 1. Torrent Power
- **Service Type**: `torrent_power`
- **Fields**: city, service_number, t_no, applicant_name, mobile, email, application_type
- **Website**: connect.torrentpower.com

### 2. Adani Gas
- **Service Type**: `adani_gas`
- **Fields**: city, consumer_number, bp_number, applicant_name, mobile, email, application_type
- **Website**: adanigas.com

### 3. AMC Water
- **Service Type**: `amc_water`
- **Fields**: zone, connection_id, applicant_name, mobile, email, application_type
- **Website**: amcwater.com

### 4. AnyRoR Gujarat
- **Service Type**: `anyror_gujarat`
- **Fields**: city, survey_number, subdivision_number, applicant_name, mobile, email, application_type
- **Website**: anyror.gujarat.gov.in

## Adding New Services

To add support for a new government website:

### 1. Create Service-Specific Automation

```python
# In backend/app/services/rpa_service.py
def submit_new_service_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Setup driver
        self.setup_driver(headless=False)
        
        # Navigate to website
        self.driver.get("https://newservice.gov.in")
        
        # Fill form fields
        if data.get('field_name'):
            field = self.wait.until(EC.element_to_be_clickable((By.ID, "fieldId")))
            field.send_keys(data['field_name'])
        
        # Submit form
        submit_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".submit-btn")))
        submit_btn.click()
        
        # Extract confirmation
        confirmation = self.driver.find_element(By.CSS_SELECTOR, ".confirmation").text
        
        return {
            "success": True,
            "confirmation_number": confirmation,
            "message": "Application submitted successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        self.close_driver()
```

### 2. Update API Router

```python
# In backend/app/routers/selenium_automation.py
# Add to run_selenium_automation function
elif request.service_type == "new_service":
    result = rpa_service.submit_new_service_application(request.form_data)
```

### 3. Update Chrome Extension

```javascript
// In chrome-extension/selenium-bridge.js
// Add to sitePatterns object
'new_service': ['newservice.gov.in', 'new-service']
```

## Advanced Features

### 1. Mobile Device Emulation
```python
enhanced_selenium_service.setup_driver(mobile_emulation=True)
```

### 2. Full Page Screenshots
```python
screenshot_path = enhanced_selenium_service.take_full_page_screenshot("full_page.png")
```

### 3. Smart Form Filling
```python
success = enhanced_selenium_service.smart_wait_and_fill(
    (By.ID, "field_id"), 
    "value_to_fill"
)
```

### 4. Form Data Extraction
```python
form_data = enhanced_selenium_service.extract_form_data()
```

## Security & Safety Features

### 1. Demo-Only URLs
Your RPA service only works with demo URLs for safety:
```python
demo_url = "http://localhost:8000/demo-govt/torrent-power"
```

### 2. Screenshot Evidence
Every automation captures screenshots for audit trails.

### 3. Error Handling
Comprehensive error handling with detailed logging.

### 4. Browser Cleanup
Automatic browser cleanup to prevent resource leaks.

## Testing Your Selenium Integration

### 1. Start Your Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Your Frontend
```bash
cd frontend
npm run dev
```

### 3. Test Selenium Demo
Visit `http://localhost:3000/selenium-demo` to test all features.

### 4. Test Chrome Extension
1. Load the extension in Chrome
2. Visit a government website
3. Use the automation controls

## Troubleshooting

### Common Issues

1. **ChromeDriver Not Found**
   - Solution: webdriver-manager automatically downloads ChromeDriver

2. **Browser Won't Start**
   - Check Chrome installation
   - Try headless mode: `headless=True`

3. **Element Not Found**
   - Increase wait timeout
   - Use different locator strategies

4. **Permission Denied**
   - Check Chrome extension permissions
   - Verify CORS settings

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Optimization

### 1. Headless Mode
Use headless mode for faster automation:
```python
self.setup_driver(headless=True)
```

### 2. Disable Images
Speed up page loading:
```python
chrome_options.add_argument('--disable-images')
```

### 3. Connection Pooling
Reuse browser instances for multiple operations.

## Monitoring & Analytics

### 1. Task Progress Tracking
Real-time progress updates via WebSocket or polling.

### 2. Automation Reports
Detailed JSON reports for each automation task.

### 3. Success Metrics
Track automation success rates and performance.

## Next Steps

1. **Add More Services**: Extend support to more government websites
2. **Improve Error Handling**: Add retry mechanisms and better error recovery
3. **Add WebSocket Support**: Real-time progress updates
4. **Implement Queuing**: Handle multiple automation requests
5. **Add Analytics Dashboard**: Monitor automation performance

## Conclusion

Your portal now has a comprehensive Selenium automation system that:
- Integrates seamlessly with your existing RPA
- Provides Chrome Extension automation
- Offers advanced features like mobile emulation
- Includes safety features and error handling
- Supports multiple government services

The system is designed to be extensible, allowing you to easily add new services and features as needed.