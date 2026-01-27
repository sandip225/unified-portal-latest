"""
Selenium Automation API Router
Provides endpoints for Chrome Extension and frontend to trigger Selenium automation
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
import asyncio
import uuid
from datetime import datetime

from ..services.enhanced_selenium_service import enhanced_selenium_service
from ..services.rpa_service import rpa_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/selenium", tags=["selenium"])

# In-memory task storage (use Redis in production)
automation_tasks = {}

class AutomationRequest(BaseModel):
    service_type: str
    form_data: Dict[str, Any]
    source: str = "api"
    options: Optional[Dict[str, Any]] = {}

class AutomationResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

@router.post("/start-automation", response_model=AutomationResponse)
async def start_automation(request: AutomationRequest, background_tasks: BackgroundTasks):
    """Start Selenium automation task"""
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create task record
        task = {
            "task_id": task_id,
            "status": "queued",
            "progress": 0,
            "service_type": request.service_type,
            "form_data": request.form_data,
            "source": request.source,
            "options": request.options,
            "result": None,
            "error": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        automation_tasks[task_id] = task
        
        # Start background automation
        background_tasks.add_task(run_selenium_automation, task_id, request)
        
        logger.info(f"Started automation task {task_id} for service {request.service_type}")
        
        return AutomationResponse(
            task_id=task_id,
            status="queued",
            message="Automation task started successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to start automation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task-status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get automation task status"""
    if task_id not in automation_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = automation_tasks[task_id]
    return TaskStatus(**task)

@router.get("/active-tasks")
async def get_active_tasks():
    """Get all active automation tasks"""
    active_tasks = {
        task_id: task for task_id, task in automation_tasks.items()
        if task["status"] in ["queued", "running"]
    }
    return {"active_tasks": active_tasks, "count": len(active_tasks)}

@router.delete("/task/{task_id}")
async def cancel_task(task_id: str):
    """Cancel automation task"""
    if task_id not in automation_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = automation_tasks[task_id]
    if task["status"] in ["completed", "failed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Task cannot be cancelled")
    
    task["status"] = "cancelled"
    task["updated_at"] = datetime.now()
    
    return {"message": "Task cancelled successfully"}

@router.post("/extract-form-data")
async def extract_form_data(url: str, options: Optional[Dict[str, Any]] = {}):
    """Extract form data from a webpage using Selenium"""
    try:
        # Setup driver
        enhanced_selenium_service.setup_driver(
            headless=options.get("headless", True),
            mobile_emulation=options.get("mobile_emulation", False)
        )
        
        # Navigate to URL
        enhanced_selenium_service.driver.get(url)
        enhanced_selenium_service.wait_for_page_load()
        
        # Extract form data
        form_data = enhanced_selenium_service.extract_form_data()
        
        # Take screenshot
        screenshot_path = f"screenshots/extract_{int(datetime.now().timestamp())}.png"
        enhanced_selenium_service.take_screenshot(screenshot_path)
        
        # Close driver
        enhanced_selenium_service.close_driver()
        
        return {
            "success": True,
            "form_data": form_data,
            "screenshot_path": screenshot_path,
            "url": url
        }
        
    except Exception as e:
        logger.error(f"Failed to extract form data: {e}")
        enhanced_selenium_service.close_driver()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-site")
async def validate_site(url: str):
    """Validate if a site is supported for automation"""
    supported_sites = {
        "torrent_power": ["torrentpower.com", "connect.torrentpower"],
        "adani_gas": ["adanigas.com", "adani-gas"],
        "amc_water": ["amcwater.com", "amc-water"],
        "anyror_gujarat": ["anyror.gujarat.gov.in", "anyror"],
        "dgvcl": ["dgvcl.com", "dgvcl.co.in"],
        "guvnl": ["guvnl.com", "guvnl.co.in"],
        "gujarat_gas": ["gujaratgas.com", "gujarat-gas"]
    }
    
    url_lower = url.lower()
    detected_service = None
    
    for service, patterns in supported_sites.items():
        if any(pattern in url_lower for pattern in patterns):
            detected_service = service
            break
    
    return {
        "supported": detected_service is not None,
        "service_type": detected_service,
        "url": url
    }

@router.get("/supported-services")
async def get_supported_services():
    """Get list of supported services for automation"""
    services = [
        {
            "service_type": "torrent_power",
            "name": "Torrent Power",
            "description": "Electricity bill payment and new connection",
            "fields": ["city", "service_number", "t_no", "applicant_name", "mobile", "email", "application_type"]
        },
        {
            "service_type": "adani_gas",
            "name": "Adani Gas",
            "description": "Gas connection and bill payment",
            "fields": ["city", "consumer_number", "bp_number", "applicant_name", "mobile", "email", "application_type"]
        },
        {
            "service_type": "amc_water",
            "name": "AMC Water",
            "description": "Water connection and bill payment",
            "fields": ["zone", "connection_id", "applicant_name", "mobile", "email", "application_type"]
        },
        {
            "service_type": "anyror_gujarat",
            "name": "AnyRoR Gujarat",
            "description": "Property records and land documents",
            "fields": ["city", "survey_number", "subdivision_number", "applicant_name", "mobile", "email", "application_type"]
        }
    ]
    
    return {"services": services}

async def run_selenium_automation(task_id: str, request: AutomationRequest):
    """Background task to run Selenium automation"""
    try:
        # Update task status
        task = automation_tasks[task_id]
        task["status"] = "running"
        task["progress"] = 10
        task["updated_at"] = datetime.now()
        
        logger.info(f"Running automation for task {task_id}, service: {request.service_type}")
        
        # Route to appropriate service
        if request.service_type == "torrent_power":
            result = rpa_service.submit_torrent_power_application(request.form_data)
        elif request.service_type == "adani_gas":
            result = rpa_service.submit_adani_gas_application(request.form_data)
        elif request.service_type == "amc_water":
            result = rpa_service.submit_amc_water_application(request.form_data)
        elif request.service_type == "anyror_gujarat":
            result = rpa_service.submit_anyror_gujarat_application(request.form_data)
        else:
            raise ValueError(f"Unsupported service type: {request.service_type}")
        
        # Update task with result
        task["status"] = "completed" if result.get("success") else "failed"
        task["progress"] = 100
        task["result"] = result
        task["updated_at"] = datetime.now()
        
        if not result.get("success"):
            task["error"] = result.get("error", "Unknown error")
        
        logger.info(f"Automation task {task_id} completed with status: {task['status']}")
        
    except Exception as e:
        logger.error(f"Automation task {task_id} failed: {e}")
        
        # Update task with error
        task = automation_tasks[task_id]
        task["status"] = "failed"
        task["error"] = str(e)
        task["updated_at"] = datetime.now()

@router.get("/health")
async def health_check():
    """Health check endpoint for Selenium service"""
    return {
        "status": "healthy",
        "service": "selenium_automation",
        "timestamp": datetime.now().isoformat(),
        "active_tasks": len([t for t in automation_tasks.values() if t["status"] == "running"])
    }