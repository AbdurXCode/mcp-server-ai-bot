"""LLM Agent for natural language interaction with MCP tools"""

import requests
import google.generativeai as genai
import os
from typing import Dict, Any, Optional
from app.core.config import settings


class LLMAgent:
    """LLM Agent that interfaces with Gemini and MCP tools"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment variables")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.mcp_base_url = f"http://{settings.server_host}:{settings.server_port}"
    
    def call_mcp_tool(self, file_number: str) -> Dict[str, Any]:
        """Call the local MCP tool to get user details"""
        url = f"{self.mcp_base_url}/test/get_user_details"
        try:
            response = requests.post(
                url, 
                json={"file_number": file_number},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Failed to call MCP tool: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def summarize_with_gemini(self, file_number: str) -> str:
        """Fetch user details from MCP, summarize via Gemini LLM"""
        try:
            # Get data from MCP tool
            mcp_data = self.call_mcp_tool(file_number)
            
            if not mcp_data.get("success", False):
                return f"❌ Error fetching user data: {mcp_data.get('error', 'Unknown error')}"
            
            # Extract the useful part of the data
            payload = mcp_data.get("data", {}).get("payload", {})
            
            if not payload:
                return "❌ No user data found for the provided file number."
            
            # Create a comprehensive prompt for Gemini
            prompt = f"""
            You are a helpful debt collection assistant. Here is user data fetched from our system:
            
            User Information:
            - Name: {payload.get('name', 'N/A')}
            - First Name: {payload.get('first_name', 'N/A')}
            - Email: {payload.get('email', 'N/A')}
            - Phone: {payload.get('phone', 'N/A')}
            - Current Amount Due: ${payload.get('current_amount', 0):.2f}
            - Last Payment: {payload.get('last_payment', 'No recent payments')}
            - Debt Summary: {payload.get('debt_summary', 'N/A')}
            - Charge Date: {payload.get('charge_date', 'N/A')}
            - File Status: {payload.get('file_Status', 'N/A')}
            - Year of Birth: {payload.get('year_of_birth', 'N/A')}
            - Zip Code: {payload.get('zip_code', 'N/A')}
            - Client Name: {payload.get('client_name', 'N/A')}
            
            Please provide a clear, professional, and empathetic summary of this customer's account status. 
            Focus on:
            1. Customer identification
            2. Current balance and debt details
            3. Payment history
            4. Any relevant account status information
            
            Format your response in a way that would be helpful for a debt collection agent to understand the customer's situation quickly.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Error processing with Gemini: {str(e)}"
    
    def chat_with_gemini(self, user_message: str, file_number: Optional[str] = None) -> str:
        """Handle natural language chat with Gemini, optionally using MCP data"""
        try:
            if file_number:
                # Get user data first
                mcp_data = self.call_mcp_tool(file_number)
                
                if mcp_data.get("success", False):
                    payload = mcp_data.get("data", {}).get("payload", {})
                    
                    # Create context-aware prompt
                    prompt = f"""
                    You are a helpful debt collection assistant. A user is asking: "{user_message}"
                    
                    Here is the relevant customer data from our system:
                    - Name: {payload.get('name', 'N/A')}
                    - Current Amount Due: ${payload.get('current_amount', 0):.2f}
                    - Email: {payload.get('email', 'N/A')}
                    - Phone: {payload.get('phone', 'N/A')}
                    - Debt Summary: {payload.get('debt_summary', 'N/A')}
                    - Last Payment: {payload.get('last_payment', 'No recent payments')}
                    - File Status: {payload.get('file_Status', 'N/A')}
                    
                    Please provide a helpful, professional response based on this customer's information.
                    Be empathetic and focus on helping resolve the debt situation.
                    """
                else:
                    prompt = f"""
                    You are a helpful debt collection assistant. A user is asking: "{user_message}"
                    
                    However, I couldn't retrieve the customer data for file number {file_number}.
                    Please respond professionally and suggest they verify the file number or contact support.
                    """
            else:
                # General chat without specific customer data
                prompt = f"""
                You are a helpful debt collection assistant. A user is asking: "{user_message}"
                
                Please provide a helpful, professional response. If they need to look up specific customer information,
                ask them to provide their file number.
                """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Error processing chat: {str(e)}"


# Global LLM agent instance
llm_agent = LLMAgent()
