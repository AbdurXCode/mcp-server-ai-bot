import google.generativeai as genai
from typing import Dict, Any, Optional
import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.tools import DebtCollectionTools
from mcp_server.config import config


class MCPClient:
    """MCP Client that integrates with Gemini LLM"""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize tools
        self.tools = DebtCollectionTools()
        self.tool_definitions = self.tools.get_tool_definitions()
        
        # System prompt
        self.system_prompt = """You are an AI assistant for a debt collection company. 
You have access to tools that can retrieve client information from the database.

Available Tools:
1. get_user_details_by_file_number(file_number): Retrieves complete client details
2. get_client_email(file_number): Gets just the email address for a client

When a user asks about a client or file number:
1. Use the appropriate tool to fetch the information
2. Present the information in a clear, professional manner
3. Be helpful and courteous

Always extract file numbers from user queries and use the tools to get accurate information.
If the user asks for specific information like email, use the most efficient tool.
"""
    
    async def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query through Gemini with MCP tool access
        
        Args:
            user_query: The user's question
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Step 1: Send query to Gemini to determine tool usage
            analysis_prompt = f"""{self.system_prompt}

User Query: {user_query}

Analyze this query and determine:
1. Does it require tool usage?
2. Which tool should be used?
3. What parameters are needed?

Respond in JSON format:
{{
    "needs_tool": true/false,
    "tool_name": "tool_name or null",
    "parameters": {{"param": "value"}},
    "reasoning": "explanation"
}}
"""
            
            response = await self._call_gemini(analysis_prompt)
            analysis = self._parse_json_response(response)
            
            # Step 2: Execute tool if needed
            tool_result = None
            if analysis.get("needs_tool") and analysis.get("tool_name"):
                tool_result = await self._execute_tool(
                    analysis["tool_name"],
                    analysis.get("parameters", {})
                )
            
            # Step 3: Generate final response
            final_prompt = f"""{self.system_prompt}

User Query: {user_query}

Tool Execution Result:
{json.dumps(tool_result, indent=2) if tool_result else "No tool was used"}

Based on the above information, provide a helpful, natural language response to the user.
Be professional, clear, and include all relevant details from the tool result.
"""
            
            final_response = await self._call_gemini(final_prompt)
            
            return {
                "success": True,
                "response": final_response,
                "tool_used": analysis.get("tool_name"),
                "tool_result": tool_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request."
            }
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from Gemini response"""
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            return {}
        except:
            return {}
    
    async def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute MCP tool"""
        if tool_name == "get_user_details_by_file_number":
            return await self.tools.get_user_details_by_file_number(
                parameters.get("file_number", "")
            )
        elif tool_name == "get_client_email":
            return await self.tools.get_client_email(
                parameters.get("file_number", "")
            )
        return None