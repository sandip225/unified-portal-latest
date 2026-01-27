"""
User Data Service for Selenium Automation
Stores and retrieves user data for form filling
"""
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import os

logger = logging.getLogger(__name__)

class UserDataService:
    """Service to store and retrieve user data for automation"""
    
    def __init__(self):
        self.data_dir = "user_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def _generate_user_key(self, mobile: str, email: str = None) -> str:
        """Generate unique key for user based on mobile and email"""
        identifier = f"{mobile}_{email or 'no_email'}"
        return hashlib.md5(identifier.encode()).hexdigest()
    
    def _get_user_file_path(self, user_key: str) -> str:
        """Get file path for user data"""
        return os.path.join(self.data_dir, f"user_{user_key}.json")
    
    def store_user_data(self, mobile: str, form_data: Dict[str, Any], 
                       email: str = None, expire_hours: int = 24) -> str:
        """
        Store user data for automation
        
        Args:
            mobile: User's mobile number (primary identifier)
            form_data: Form data to store
            email: User's email (secondary identifier)
            expire_hours: Hours after which data expires
            
        Returns:
            user_key: Unique key for retrieving data
        """
        try:
            user_key = self._generate_user_key(mobile, email)
            file_path = self._get_user_file_path(user_key)
            
            # Prepare data with metadata
            user_data = {
                "user_key": user_key,
                "mobile": mobile,
                "email": email,
                "form_data": form_data,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=expire_hours)).isoformat(),
                "last_used": datetime.now().isoformat(),
                "usage_count": 1
            }
            
            # Check if user data already exists
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                    user_data["usage_count"] = existing_data.get("usage_count", 0) + 1
                    user_data["created_at"] = existing_data.get("created_at", user_data["created_at"])
                except:
                    pass
            
            # Save user data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"User data stored for key: {user_key}")
            return user_key
            
        except Exception as e:
            logger.error(f"Failed to store user data: {e}")
            raise e
    
    def retrieve_user_data(self, user_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user data by key
        
        Args:
            user_key: Unique key for user data
            
        Returns:
            User data if found and not expired, None otherwise
        """
        try:
            file_path = self._get_user_file_path(user_key)
            
            if not os.path.exists(file_path):
                logger.warning(f"User data not found for key: {user_key}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            
            # Check if data has expired
            expires_at = datetime.fromisoformat(user_data["expires_at"])
            if datetime.now() > expires_at:
                logger.warning(f"User data expired for key: {user_key}")
                # Clean up expired data
                os.remove(file_path)
                return None
            
            # Update last used timestamp
            user_data["last_used"] = datetime.now().isoformat()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"User data retrieved for key: {user_key}")
            return user_data
            
        except Exception as e:
            logger.error(f"Failed to retrieve user data: {e}")
            return None
    
    def find_user_by_mobile(self, mobile: str) -> Optional[Dict[str, Any]]:
        """
        Find user data by mobile number
        
        Args:
            mobile: User's mobile number
            
        Returns:
            User data if found, None otherwise
        """
        try:
            # Try with no email first
            user_key = self._generate_user_key(mobile)
            user_data = self.retrieve_user_data(user_key)
            
            if user_data:
                return user_data
            
            # If not found, search through all user files
            for filename in os.listdir(self.data_dir):
                if filename.startswith("user_") and filename.endswith(".json"):
                    file_path = os.path.join(self.data_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        if data.get("mobile") == mobile:
                            # Check if expired
                            expires_at = datetime.fromisoformat(data["expires_at"])
                            if datetime.now() <= expires_at:
                                return data
                            else:
                                # Clean up expired data
                                os.remove(file_path)
                    except:
                        continue
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to find user by mobile: {e}")
            return None
    
    def update_user_data(self, user_key: str, form_data: Dict[str, Any]) -> bool:
        """
        Update existing user data
        
        Args:
            user_key: Unique key for user data
            form_data: Updated form data
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            existing_data = self.retrieve_user_data(user_key)
            if not existing_data:
                return False
            
            # Update form data and metadata
            existing_data["form_data"].update(form_data)
            existing_data["last_used"] = datetime.now().isoformat()
            existing_data["usage_count"] = existing_data.get("usage_count", 0) + 1
            
            # Save updated data
            file_path = self._get_user_file_path(user_key)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"User data updated for key: {user_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user data: {e}")
            return False
    
    def delete_user_data(self, user_key: str) -> bool:
        """
        Delete user data
        
        Args:
            user_key: Unique key for user data
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            file_path = self._get_user_file_path(user_key)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"User data deleted for key: {user_key}")
                return True
            else:
                logger.warning(f"User data not found for deletion: {user_key}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete user data: {e}")
            return False
    
    def cleanup_expired_data(self) -> int:
        """
        Clean up expired user data files
        
        Returns:
            Number of files cleaned up
        """
        cleaned_count = 0
        
        try:
            for filename in os.listdir(self.data_dir):
                if filename.startswith("user_") and filename.endswith(".json"):
                    file_path = os.path.join(self.data_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        expires_at = datetime.fromisoformat(data["expires_at"])
                        if datetime.now() > expires_at:
                            os.remove(file_path)
                            cleaned_count += 1
                            logger.info(f"Cleaned expired data: {filename}")
                    except:
                        # Remove corrupted files
                        os.remove(file_path)
                        cleaned_count += 1
                        logger.info(f"Cleaned corrupted data: {filename}")
            
            logger.info(f"Cleanup completed. Removed {cleaned_count} files.")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired data: {e}")
            return cleaned_count
    
    def get_user_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored user data
        
        Returns:
            Statistics dictionary
        """
        try:
            stats = {
                "total_users": 0,
                "active_users": 0,
                "expired_users": 0,
                "total_usage": 0,
                "most_used_fields": {},
                "recent_activity": []
            }
            
            for filename in os.listdir(self.data_dir):
                if filename.startswith("user_") and filename.endswith(".json"):
                    file_path = os.path.join(self.data_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        stats["total_users"] += 1
                        stats["total_usage"] += data.get("usage_count", 0)
                        
                        # Check if expired
                        expires_at = datetime.fromisoformat(data["expires_at"])
                        if datetime.now() > expires_at:
                            stats["expired_users"] += 1
                        else:
                            stats["active_users"] += 1
                        
                        # Track field usage
                        for field_name in data.get("form_data", {}).keys():
                            stats["most_used_fields"][field_name] = stats["most_used_fields"].get(field_name, 0) + 1
                        
                        # Recent activity
                        stats["recent_activity"].append({
                            "user_key": data["user_key"][:8] + "...",  # Partial key for privacy
                            "last_used": data.get("last_used"),
                            "usage_count": data.get("usage_count", 0)
                        })
                        
                    except:
                        continue
            
            # Sort recent activity
            stats["recent_activity"].sort(key=lambda x: x["last_used"], reverse=True)
            stats["recent_activity"] = stats["recent_activity"][:10]  # Top 10
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get user stats: {e}")
            return {}

# Global service instance
user_data_service = UserDataService()