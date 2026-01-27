"""
Unified Automation Router
Handles both direct automation and login-assisted automation
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
import json
from datetime import datetime

from ..services.direct_automation_service import direct_automation_service
from ..services.login_assisted_service import login_assisted_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/unified-automation", tags=["unified-automation"])

class AutomationRequest(BaseModel):
    supplier_id: str
    service_type: str  # "name_change", "address_change", etc.
    form_data: Dict[str, Any]
    automation_preference: str = "auto"  # "auto", "direct", "assisted"

class AutomationResponse(BaseModel):
    success: bool
    automation_type: str  # "direct", "login_assisted", "manual_only"
    message: str
    instructions: Optional[List[str]] = None
    screenshot_path: Optional[str] = None
    next_steps: Optional[List[str]] = None

# Supplier automation configuration
SUPPLIER_CONFIG = {
    # GAS SUPPLIERS - DIRECT ACCESS (No login required)
    "gujarat-gas": {
        "automation_type": "direct",
        "login_required": False,
        "service_method": "submit_gujarat_gas_name_change",
        "instructions": [
            "Gujarat Gas allows direct name change requests",
            "Form will be filled automatically",
            "Manual verification and submission required"
        ]
    },
    "vadodara-gas": {
        "automation_type": "direct", 
        "login_required": False,
        "service_method": "submit_vadodara_gas_name_change",
        "instructions": [
            "Vadodara Gas direct form access",
            "Automatic form filling available"
        ]
    },
    "torrent-gas": {
        "automation_type": "direct",
        "login_required": False, 
        "service_method": "submit_torrent_power_name_change",
        "instructions": [
            "Torrent Gas PDF form download",
            "Manual form filling required after download"
        ]
    },
    
    # GAS SUPPLIERS - LOGIN REQUIRED
    "adani-gas": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "customer_portal_otp",
        "service_method": "assist_adani_gas_login_and_fill",
        "instructions": [
            "Login to Adani Gas customer portal required",
            "OTP verification needed",
            "Form will be filled after successful login"
        ]
    },
    
    # ELECTRICITY SUPPLIERS - LOGIN REQUIRED
    "pgvcl": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "guvnl_portal",
        "service_method": "assist_guvnl_login_and_fill",
        "instructions": [
            "Login to GUVNL portal required",
            "CAPTCHA and OTP verification needed",
            "Form will be filled after successful login"
        ]
    },
    "ugvcl": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "guvnl_portal",
        "service_method": "assist_guvnl_login_and_fill",
        "instructions": [
            "Login to GUVNL portal required",
            "CAPTCHA and OTP verification needed", 
            "Form will be filled after successful login"
        ]
    },
    "mgvcl": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "guvnl_portal",
        "service_method": "assist_guvnl_login_and_fill",
        "instructions": [
            "Login to GUVNL portal required",
            "CAPTCHA and OTP verification needed",
            "Form will be filled after successful login"
        ]
    },
    "dgvcl": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "guvnl_portal", 
        "service_method": "assist_guvnl_login_and_fill",
        "instructions": [
            "Login to GUVNL portal required",
            "CAPTCHA and OTP verification needed",
            "Form will be filled after successful login"
        ]
    },
    
    # ELECTRICITY SUPPLIERS - DIRECT ACCESS
    "torrent-power": {
        "automation_type": "direct",
        "login_required": False,
        "service_method": "submit_torrent_power_name_change", 
        "instructions": [
            "Torrent Power PDF form available",
            "Download and manual filling required"
        ]
    },
    
    # WATER SUPPLIERS - DIRECT ACCESS
    "gwssb": {
        "automation_type": "direct",
        "login_required": False,
        "service_method": "submit_gwssb_name_change",
        "instructions": [
            "GWSSB direct form access available",
            "Automatic form filling supported"
        ]
    },
    
    # WATER SUPPLIERS - LOGIN/VERIFICATION REQUIRED
    "amc": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "ward_verification",
        "service_method": "assist_municipal_water_login",
        "instructions": [
            "AMC ward verification required",
            "Login or connection verification needed",
            "Form assistance available after verification"
        ]
    },
    "smc": {
        "automation_type": "login_assisted", 
        "login_required": True,
        "auth_method": "ward_verification",
        "service_method": "assist_municipal_water_login",
        "instructions": [
            "SMC manual approval process",
            "Ward office verification required"
        ]
    },
    "vmc": {
        "automation_type": "manual_only",
        "login_required": False,
        "service_method": None,
        "instructions": [
            "VMC - Offline only process",
            "Visit ward office for name change"
        ]
    },
    "rmc": {
        "automation_type": "manual_only",
        "login_required": False, 
        "service_method": None,
        "instructions": [
            "RMC - Offline only process",
            "Visit ward office for name change"
        ]
    },
    
    # PROPERTY SUPPLIERS - DIRECT ACCESS
    "anyror": {
        "automation_type": "direct",
        "login_required": False,
        "service_method": "submit_anyror_name_change",
        "instructions": [
            "AnyROR public record view available",
            "For name change, visit e-Dhara center or Talati office"
        ]
    },
    
    # PROPERTY SUPPLIERS - LOGIN REQUIRED
    "enagar": {
        "automation_type": "login_assisted",
        "login_required": True,
        "auth_method": "citizen_login",
        "service_method": None,
        "instructions": [
            "e-Nagar citizen login required",
            "Manual process after login"
        ]
    }
}

@router.post("/start-automation", response_model=AutomationResponse)
async def start_unified_automation(request: AutomationRequest):
    """Start unified automation based on supplier configuration"""
    try:
        supplier_config = SUPPLIER_CONFIG.get(request.supplier_id)
        
        if not supplier_config:
            raise HTTPException(
                status_code=400, 
                detail=f"Supplier '{request.supplier_id}' not supported for automation"
            )
        
        automation_type = supplier_config["automation_type"]
        
        # Handle different automation types
        if automation_type == "direct":
            return await handle_direct_automation(request, supplier_config)
        elif automation_type == "login_assisted":
            return await handle_login_assisted_automation(request, supplier_config)
        elif automation_type == "manual_only":
            return AutomationResponse(
                success=False,
                automation_type="manual_only",
                message=f"{request.supplier_id} requires manual process only",
                instructions=supplier_config["instructions"],
                next_steps=[
                    "Visit the respective office",
                    "Carry required documents",
                    "Complete the process manually"
                ]
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid automation type")
            
    except Exception as e:
        logger.error(f"Unified automation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_direct_automation(request: AutomationRequest, config: Dict[str, Any]) -> AutomationResponse:
    """Handle direct automation (no login required)"""
    try:
        service_method = config["service_method"]
        
        # Route to appropriate direct automation method
        if service_method == "submit_gujarat_gas_name_change":
            result = direct_automation_service.submit_gujarat_gas_name_change(request.form_data)
        elif service_method == "submit_vadodara_gas_name_change":
            result = direct_automation_service.submit_vadodara_gas_name_change(request.form_data)
        elif service_method == "submit_torrent_power_name_change":
            result = direct_automation_service.submit_torrent_power_name_change(request.form_data)
        elif service_method == "submit_gwssb_name_change":
            result = direct_automation_service.submit_gwssb_name_change(request.form_data)
        elif service_method == "submit_anyror_name_change":
            result = direct_automation_service.submit_anyror_name_change(request.form_data)
        else:
            raise ValueError(f"Unknown direct automation method: {service_method}")
        
        return AutomationResponse(
            success=result["success"],
            automation_type="direct",
            message=result["message"],
            instructions=config["instructions"],
            screenshot_path=result.get("screenshot_path"),
            next_steps=[
                "Review the filled form",
                "Verify all information is correct", 
                "Submit the form manually",
                "Save confirmation number"
            ]
        )
        
    except Exception as e:
        logger.error(f"Direct automation failed: {e}")
        return AutomationResponse(
            success=False,
            automation_type="direct",
            message=f"Direct automation failed: {str(e)}",
            instructions=config["instructions"]
        )

async def handle_login_assisted_automation(request: AutomationRequest, config: Dict[str, Any]) -> AutomationResponse:
    """Handle login-assisted automation (login required)"""
    try:
        service_method = config["service_method"]
        
        # Route to appropriate login-assisted method
        if service_method == "assist_guvnl_login_and_fill":
            # Determine GUVNL service type
            service_type = request.supplier_id.upper()  # PGVCL, UGVCL, etc.
            result = login_assisted_service.assist_guvnl_login_and_fill(request.form_data, service_type)
        elif service_method == "assist_adani_gas_login_and_fill":
            result = login_assisted_service.assist_adani_gas_login_and_fill(request.form_data)
        elif service_method == "assist_municipal_water_login":
            city = request.supplier_id.upper()  # AMC, SMC, etc.
            result = login_assisted_service.assist_municipal_water_login(request.form_data, city)
        else:
            raise ValueError(f"Unknown login-assisted method: {service_method}")
        
        return AutomationResponse(
            success=result["success"],
            automation_type="login_assisted",
            message=result["message"],
            instructions=config["instructions"],
            screenshot_path=result.get("screenshot_path"),
            next_steps=[
                "Complete login process manually",
                "Solve CAPTCHA if required",
                "Enter OTP if required",
                "Review auto-filled form",
                "Submit after verification"
            ]
        )
        
    except Exception as e:
        logger.error(f"Login-assisted automation failed: {e}")
        return AutomationResponse(
            success=False,
            automation_type="login_assisted", 
            message=f"Login-assisted automation failed: {str(e)}",
            instructions=config["instructions"]
        )

@router.get("/supplier-info/{supplier_id}")
async def get_supplier_automation_info(supplier_id: str):
    """Get automation information for a specific supplier"""
    config = SUPPLIER_CONFIG.get(supplier_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return {
        "supplier_id": supplier_id,
        "automation_type": config["automation_type"],
        "login_required": config["login_required"],
        "auth_method": config.get("auth_method"),
        "instructions": config["instructions"],
        "supported": config["service_method"] is not None
    }

@router.get("/supported-suppliers")
async def get_supported_suppliers():
    """Get list of all supported suppliers with their automation capabilities"""
    suppliers = []
    
    for supplier_id, config in SUPPLIER_CONFIG.items():
        suppliers.append({
            "supplier_id": supplier_id,
            "automation_type": config["automation_type"],
            "login_required": config["login_required"],
            "supported": config["service_method"] is not None,
            "instructions": config["instructions"]
        })
    
    return {
        "suppliers": suppliers,
        "total_count": len(suppliers),
        "direct_automation": len([s for s in suppliers if s["automation_type"] == "direct"]),
        "login_assisted": len([s for s in suppliers if s["automation_type"] == "login_assisted"]),
        "manual_only": len([s for s in suppliers if s["automation_type"] == "manual_only"])
    }

@router.get("/automation-stats")
async def get_automation_statistics():
    """Get automation statistics and capabilities"""
    stats = {
        "total_suppliers": len(SUPPLIER_CONFIG),
        "direct_automation": 0,
        "login_assisted": 0, 
        "manual_only": 0,
        "by_category": {
            "gas": {"direct": 0, "login_assisted": 0, "manual_only": 0},
            "electricity": {"direct": 0, "login_assisted": 0, "manual_only": 0},
            "water": {"direct": 0, "login_assisted": 0, "manual_only": 0},
            "property": {"direct": 0, "login_assisted": 0, "manual_only": 0}
        }
    }
    
    # Category mapping
    category_mapping = {
        "gujarat-gas": "gas", "adani-gas": "gas", "vadodara-gas": "gas", "torrent-gas": "gas",
        "pgvcl": "electricity", "ugvcl": "electricity", "mgvcl": "electricity", "dgvcl": "electricity", "torrent-power": "electricity",
        "gwssb": "water", "amc": "water", "smc": "water", "vmc": "water", "rmc": "water",
        "anyror": "property", "enagar": "property"
    }
    
    for supplier_id, config in SUPPLIER_CONFIG.items():
        automation_type = config["automation_type"]
        category = category_mapping.get(supplier_id, "other")
        
        stats[automation_type] += 1
        if category in stats["by_category"]:
            stats["by_category"][category][automation_type] += 1
    
    return stats