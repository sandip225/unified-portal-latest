"""
Production-Ready Torrent Power Automation API
Handles the complete workflow from Unified Portal to Official Website
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime

from app.services.torrent_power_automation import get_torrent_automation_service
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api/torrent-automation", tags=["Torrent Power Automation"])


class TorrentAutomationRequest(BaseModel):
    """Request model for Torrent Power automation"""
    city: str = "Ahmedabad"
    service_number: str
    t_number: str  # Transaction Number
    mobile: str
    email: str
    confirm_email: Optional[str] = None


class TorrentAutomationResponse(BaseModel):
    """Response model for automation results"""
    success: bool
    message: str
    details: Optional[str] = None
    timestamp: str
    provider: str = "torrent_power"
    automation_type: str = "production_ai_selenium"
    session_data: Optional[Dict[str, Any]] = None
    screenshots: Optional[list] = None
    fields_filled: Optional[int] = None
    total_fields: Optional[int] = None
    success_rate: Optional[str] = None
    next_steps: Optional[list] = None
    portal_url: str = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
    error: Optional[str] = None


@router.post("/start-automation", response_model=TorrentAutomationResponse)
async def start_torrent_power_automation(
    request: TorrentAutomationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Start the complete Torrent Power automation workflow
    Following the production-ready prompt specifications
    """
    
    try:
        print("🚀 PRODUCTION Torrent Power automation request received")
        print(f"👤 User: {current_user.email}")
        print(f"📋 Request data: {request.dict()}")
        
        # Validate required fields
        if not request.service_number:
            raise HTTPException(
                status_code=400,
                detail="Service Number is required for Torrent Power automation"
            )
        
        if not request.t_number:
            raise HTTPException(
                status_code=400,
                detail="Transaction Number (T No) is required for Torrent Power automation"
            )
        
        if not request.mobile or len(request.mobile) != 10:
            raise HTTPException(
                status_code=400,
                detail="Valid 10-digit mobile number is required"
            )
        
        if not request.email:
            raise HTTPException(
                status_code=400,
                detail="Email address is required for Torrent Power automation"
            )
        
        # Get automation service
        print("🤖 Initializing Torrent Power automation service...")
        automation_service = get_torrent_automation_service()
        
        # Prepare user data
        user_data = {
            'city': request.city,
            'service_number': request.service_number,
            't_number': request.t_number,
            'mobile': request.mobile,
            'email': request.email,
            'user_id': current_user.id,
            'user_email': current_user.email
        }
        
        print("🚀 Starting complete automation workflow...")
        
        # Execute the complete workflow
        result = await automation_service.execute_complete_workflow(user_data)
        
        print(f"📊 Automation completed with result: {result.get('success', False)}")
        
        # Return structured response
        return TorrentAutomationResponse(
            success=result.get("success", False),
            message=result.get("message", "Automation completed"),
            details=result.get("details", ""),
            timestamp=result.get("timestamp", datetime.now().isoformat()),
            session_data=result.get("session_data", {}),
            screenshots=result.get("screenshots", []),
            fields_filled=result.get("fields_filled", 0),
            total_fields=result.get("total_fields", 0),
            success_rate=result.get("success_rate", "0%"),
            next_steps=result.get("next_steps", []),
            error=result.get("error")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Torrent automation API error: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        return TorrentAutomationResponse(
            success=False,
            message=f"Failed to start Torrent Power automation: {str(e)}",
            timestamp=datetime.now().isoformat(),
            error=str(e),
            details=traceback.format_exc()
        )


@router.get("/test-connection")
async def test_automation_connection():
    """
    Test if the automation service is working
    """
    
    try:
        automation_service = get_torrent_automation_service()
        
        # Test driver creation
        if automation_service.create_driver():
            # Close test driver
            if automation_service.driver:
                automation_service.driver.quit()
            
            return {
                "success": True,
                "message": "Torrent Power automation service is ready",
                "timestamp": datetime.now().isoformat(),
                "automation_type": "production_ai_selenium",
                "browser": "Chrome with Selenium WebDriver",
                "features": [
                    "✅ AI-assisted field mapping",
                    "✅ Intelligent form filling",
                    "✅ Screenshot audit trail",
                    "✅ Fallback strategies",
                    "✅ Production-ready error handling"
                ]
            }
        else:
            return {
                "success": False,
                "message": "Failed to initialize Chrome driver",
                "timestamp": datetime.now().isoformat(),
                "error": "Browser driver initialization failed"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Automation service test failed",
            "timestamp": datetime.now().isoformat()
        }


@router.get("/supported-fields")
async def get_supported_fields():
    """
    Get the list of supported fields for Torrent Power automation
    """
    
    return {
        "success": True,
        "provider": "torrent_power",
        "automation_type": "production_ai_selenium",
        "supported_fields": {
            "city": {
                "type": "dropdown",
                "required": True,
                "default": "Ahmedabad",
                "options": ["Ahmedabad", "Surat", "Gandhinagar", "Bhavnagar"],
                "description": "City/Location for service"
            },
            "service_number": {
                "type": "text",
                "required": True,
                "pattern": "^[A-Z0-9]+$",
                "description": "Service/Consumer Number"
            },
            "t_number": {
                "type": "text", 
                "required": True,
                "pattern": "^T[0-9]+$",
                "description": "Transaction Number (T No)"
            },
            "mobile": {
                "type": "tel",
                "required": True,
                "pattern": "^[0-9]{10}$",
                "description": "10-digit mobile number"
            },
            "email": {
                "type": "email",
                "required": True,
                "description": "Email address for notifications"
            }
        },
        "workflow_steps": [
            "1. Data validation and session storage",
            "2. Navigate to official Torrent Power website", 
            "3. AI-assisted field identification and mapping",
            "4. Intelligent form filling with fallback strategies",
            "5. Screenshot audit trail generation",
            "6. Stop before submission for user control",
            "7. Provide completion summary and next steps"
        ],
        "timestamp": datetime.now().isoformat()
    }