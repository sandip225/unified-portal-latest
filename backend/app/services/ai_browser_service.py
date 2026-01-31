"""
AI Browser Automation Service using Selenium
Reliable browser automation for government portals with visible process
No AI dependencies - pure Selenium automation
"""

import asyncio
import os
from typing import Dict, Any, Optional
from datetime import datetime
import json
import traceback

# Import Selenium browser service
from app.services.selenium_browser_service import get_selenium_browser_service

from dotenv import load_dotenv
from app.config import get_settings

load_dotenv()
settings = get_settings()


class AIBrowserService:
    """Selenium-powered browser automation service"""
    
    def __init__(self):
        try:
            print("🚀 Initializing AI Browser Service with Selenium...")
            
            # Get Selenium browser service
            self.selenium_service = get_selenium_browser_service()
            
            print("✅ AI Browser Service initialized successfully with Selenium")
            
        except Exception as e:
            print(f"❌ Error initializing AI Browser Service: {str(e)}")
            print(f"❌ Traceback: {traceback.format_exc()}")
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
        
        try:
            print("🚀 Starting Torrent Power Selenium automation...")
            
            # Use Selenium service for automation
            result = await self.selenium_service.auto_fill_torrent_power_form(user_data)
            
            return result
            
        except Exception as e:
            print(f"❌ Torrent Power automation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Torrent Power automation failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "provider": "torrent_power",
                "automation_type": "selenium_direct",
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
        
        try:
            print(f"🚀 Starting {provider} Selenium automation...")
            
            # Use Selenium service for automation
            result = await self.selenium_service.auto_fill_government_portal_form(
                provider, user_data, portal_url, login_required, login_credentials
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to auto-fill {provider} form with Selenium",
                "timestamp": datetime.now().isoformat(),
                "provider": provider,
                "automation_type": "selenium_direct",
                "technology": "Selenium WebDriver"
            }
    
    async def get_form_fields(self, portal_url: str) -> Dict[str, Any]:
        """
        Analyze a portal to identify available form fields using Selenium
        
        Args:
            portal_url: URL of the portal to analyze
            
        Returns:
            Dictionary with form field information
        """
        
        try:
            print(f"🔍 Analyzing form fields for: {portal_url}")
            
            # This would use Selenium to analyze form structure
            # For now, return a basic response
            return {
                "success": True,
                "form_analysis": f"Form analysis for {portal_url} using Selenium",
                "portal_url": portal_url,
                "timestamp": datetime.now().isoformat(),
                "analysis_type": "selenium_direct",
                "technology": "Selenium WebDriver"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "portal_url": portal_url,
                "timestamp": datetime.now().isoformat(),
                "analysis_type": "selenium_direct",
                "technology": "Selenium WebDriver"
            }


# Singleton instance
ai_browser_service = None

def get_ai_browser_service():
    """Get or create the AI browser service instance"""
    global ai_browser_service
    if ai_browser_service is None:
        ai_browser_service = AIBrowserService()
    return ai_browser_service