"""MCP Tools for interacting with company API"""

import httpx
from typing import Any, Dict, List, Optional
from app.core.config import settings


class UserTools:
    """Tools for user-related operations via company API"""
    
    def __init__(self):
        self.api_url = settings.api_url
        self.api_key = settings.api_key
        self.timeout = settings.api_timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def get_user_details_by_file_number(self, file_number: str) -> Dict[str, Any]:
        """
        Retrieves user details based on the provided file number.
        This function is used when the AI agent asks the user for their file number 
        and uses it to look up relevant information such as name, contact details, 
        case status, or other associated data.
        
        Args:
            file_number: The file number to look up user details
            
        Returns:
            Dict containing user details information
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.api_url}/user-details-by-file-number",
                headers=self.headers,
                params={"file_number": file_number}
            )
            response.raise_for_status()
            return response.json()
    


# Global tool instance
user_tools = UserTools()

