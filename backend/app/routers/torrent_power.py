"""
Torrent Power RPA API Router
Provides endpoints for Torrent Power automation
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging
from app.services.torrent_power_service import torrent_power_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/torrent-power", tags=["Torrent Power RPA"])

class TorrentPowerLoginData(BaseModel):
    username: str
    password: str

class TorrentPowerFormData(BaseModel):
    city: Optional[str] = "Ahmedabad"
    service_number: Optional[str] = None
    transaction_number: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    old_name: Optional[str] = None
    new_name: Optional[str] = None

class TorrentPowerAutomationRequest(BaseModel):
    login_data: Optional[TorrentPowerLoginData] = None # Optional now for live fill
    form_data: TorrentPowerFormData

# ... existing automate_name_change ...

@router.post("/start-live-fill")
async def start_live_fill(request: TorrentPowerAutomationRequest):
    """
    Start Live Auto-fill (Headed Browser)
    
    This endpoint will:
    1. Launch browser in visible mode
    2. Navigate to Name Change URL
    3. Wait for page load (and manual login if needed)
    4. Auto-fill the form
    5. Leave browser open for user submission
    """
    try:
        logger.info("Starting Live Torrent Power Fill")
        
        # Convert Pydantic models to dictionaries
        form_data = request.form_data.dict()
        
        # Call the automation service
        result = torrent_power_service.start_live_automation(form_data)
        
        if result['success']:
            return {
                "success": True,
                "message": result['message'],
                "filled_fields": result.get('filled_fields'),
                "website": "Torrent Power",
                "service": "Name Change"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": result.get('error'),
                    "message": "Live Fill failed"
                }
            )
            
    except Exception as e:
        logger.error(f"Torrent Power Live Fill API error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Internal server error during live fill"
            }
        )

# ... existing test_connection ...

@router.get("/form-fields")
async def get_form_fields():
    """Get information about required form fields"""
    return {
        "login_fields": {
            "username": "Service number or registered username",
            "password": "Account password"
        },
        "form_fields": {
            "city": "City (default: Ahmedabad)",
            "service_number": "Torrent Power service number",
            "transaction_number": "Transaction / Reference Number",
            "mobile": "Mobile number",
            "email": "Email address",
            "old_name": "Current name on the connection",
            "new_name": "New name to be updated"
        },
        "notes": [
            "Username is typically the service number",
            "Captcha solving may require manual intervention",
            "Form will be filled but manual review is recommended before submission"
        ]
    }

@router.post("/automate-name-change")
async def automate_name_change(request: TorrentPowerAutomationRequest):
    """
    Automate Torrent Power name change process
    
    This endpoint will:
    1. Login to Torrent Power portal
    2. Navigate to name change application
    3. Fill the form with provided data
    4. Take screenshot for verification
    
    Note: Manual captcha solving may be required
    """
    try:
        logger.info("Starting Torrent Power name change automation")
        
        # Convert Pydantic models to dictionaries
        login_data = request.login_data.dict()
        form_data = request.form_data.dict()
        
        # Call the automation service
        result = torrent_power_service.automate_name_change(login_data, form_data)
        
        if result['success']:
            return {
                "success": True,
                "message": result['message'],
                "screenshot": result.get('screenshot'),
                "next_step": result.get('next_step'),
                "website": "Torrent Power",
                "service": "Name Change"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": result.get('error'),
                    "message": "Automation failed"
                }
            )
            
    except Exception as e:
        logger.error(f"Torrent Power automation API error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Internal server error during automation"
            }
        )

@router.get("/test-connection")
async def test_connection():
    """Test if Torrent Power website is accessible"""
    try:
        # Simple connectivity test
        import requests
        response = requests.get("https://connect.torrentpower.com", timeout=10)
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Torrent Power website is accessible",
                "status_code": response.status_code
            }
        else:
            return {
                "success": False,
                "message": f"Torrent Power website returned status code: {response.status_code}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to connect to Torrent Power website: {str(e)}",
            "error": str(e)
        }

@router.get("/test-rpa")
async def test_rpa():
    """Test RPA automation setup"""
    try:
        from app.services.torrent_power_service import torrent_power_service
        
        # Test if Chrome and ChromeDriver are available
        test_result = {
            "chrome_available": False,
            "chromedriver_available": False,
            "selenium_working": False,
            "error": None
        }
        
        # Test Chrome installation
        import subprocess
        try:
            chrome_version = subprocess.check_output(['google-chrome', '--version'], stderr=subprocess.STDOUT)
            test_result["chrome_available"] = True
            test_result["chrome_version"] = chrome_version.decode().strip()
        except Exception as e:
            test_result["chrome_error"] = str(e)
        
        # Test ChromeDriver installation
        try:
            chromedriver_version = subprocess.check_output(['chromedriver', '--version'], stderr=subprocess.STDOUT)
            test_result["chromedriver_available"] = True
            test_result["chromedriver_version"] = chromedriver_version.decode().strip()
        except Exception as e:
            test_result["chromedriver_error"] = str(e)
        
        # Test Selenium setup
        try:
            torrent_power_service.setup_driver()
            test_result["selenium_working"] = True
            torrent_power_service.cleanup()
        except Exception as e:
            test_result["selenium_error"] = str(e)
        
        return {
            "success": True,
            "message": "RPA test completed",
            "test_results": test_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"RPA test failed: {str(e)}",
            "error": str(e)
        }

@router.get("/form-fields")
async def get_form_fields():
    """Get information about required form fields"""
    return {
        "login_fields": {
            "username": "Service number or registered username",
            "password": "Account password"
        },
        "form_fields": {
            "city": "City (default: Ahmedabad)",
            "service_number": "Torrent Power service number",
            "mobile": "Mobile number",
            "email": "Email address",
            "old_name": "Current name on the connection",
            "new_name": "New name to be updated"
        },
        "notes": [
            "Username is typically the service number",
            "Captcha solving may require manual intervention",
            "Form will be filled but manual review is recommended before submission"
        ]
    }