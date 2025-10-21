"""MCP Server setup and configuration"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from app.core.config import settings
from app.tools.user_tools import user_tools
import json


def create_server() -> Server:
    """Create and configure MCP server instance"""
    mcp_server = Server(settings.mcp_server_name)
    
    @mcp_server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available MCP tools"""
        return [
            Tool(
                name="get_user_details_by_file_number",
                description="Retrieves user details based on the provided file number. This function is used when the AI agent asks the user for their file number and uses it to look up relevant information such as name, contact details, case status, or other associated data.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_number": {
                            "type": "string",
                            "description": "The file number to look up user details"
                        }
                    },
                    "required": ["file_number"]
                }
            )
        ]

    @mcp_server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls from MCP clients"""
        
        try:
            if name == "get_user_details_by_file_number":
                result = await user_tools.get_user_details_by_file_number(arguments["file_number"])
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}"
            )]
    
    return mcp_server


# Create server instance for direct MCP usage
mcp_server = create_server()



