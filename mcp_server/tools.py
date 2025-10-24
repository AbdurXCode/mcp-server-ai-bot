import httpx
from typing import Dict, Any
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.config import config


class DebtCollectionTools:
    """Tools for interacting with debt collection API"""
    
    def __init__(self):
        self.api_url = config.DEBT_COLLECTION_API_URL
        self.timeout = config.API_TIMEOUT
    
    async def get_user_details_by_file_number(self, file_number: str) -> Dict[str, Any]:
        """
        Retrieve user details from the debt collection system.
        
        Args:
            file_number: The file number to look up
            
        Returns:
            Dictionary containing user details or error information
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.api_url,
                    params={"file_number": file_number}
                )
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API returned status code {response.status_code}",
                        "details": response.text
                    }
                    
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Request timeout",
                "details": f"API did not respond within {self.timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Request failed",
                "details": str(e)
            }
    
    async def get_client_email(self, file_number: str) -> Dict[str, Any]:
        """
        Extract email address for a specific file number.
        
        Args:
            file_number: The file number to look up
            
        Returns:
            Dictionary containing email or error information
        """
        result = await self.get_user_details_by_file_number(file_number)
        
        if result["success"]:
            data = result["data"]
            email = data.get("email") or data.get("contact", {}).get("email")
            
            if email:
                return {
                    "success": True,
                    "email": email,
                    "file_number": file_number
                }
            else:
                return {
                    "success": False,
                    "error": "Email not found",
                    "details": "No email address in the client record"
                }
        else:
            return result
    
    def get_tool_definitions(self):
        """Return MCP tool definitions"""
        return [
            {
                "name": "get_user_details_by_file_number",
                "description": (
                    "Retrieves user details based on the provided file number. "
                    "This function is used when the AI agent asks the user for "
                    "their file number and uses it to look up relevant information "
                    "such as name, contact details, case status, or other associated data."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_number": {
                            "type": "string",
                            "description": "The file number to retrieve details for (e.g., '123421')"
                        }
                    },
                    "required": ["file_number"]
                }
            },
            {
                "name": "get_client_email",
                "description": (
                    "Extracts and returns the email address for a client "
                    "based on their file number."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_number": {
                            "type": "string",
                            "description": "The file number to retrieve email for"
                        }
                    },
                    "required": ["file_number"]
                }
            }
        ]