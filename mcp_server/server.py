import asyncio
import json
from typing import Any, Dict, List
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp_server.tools import DebtCollectionTools
from mcp_server.config import config


class DebtCollectionMCPServer:
    """MCP Server for Debt Collection System"""
    
    def __init__(self):
        self.server = Server("debt-collection-mcp")
        self.tools = DebtCollectionTools()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            tool_defs = self.tools.get_tool_definitions()
            return [
                Tool(
                    name=tool["name"],
                    description=tool["description"],
                    inputSchema=tool["parameters"]
                )
                for tool in tool_defs
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute tool calls"""
            
            if name == "get_user_details_by_file_number":
                file_number = arguments.get("file_number")
                if not file_number:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "file_number parameter is required"
                        })
                    )]
                
                result = await self.tools.get_user_details_by_file_number(file_number)
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            
            elif name == "get_client_email":
                file_number = arguments.get("file_number")
                if not file_number:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "file_number parameter is required"
                        })
                    )]
                
                result = await self.tools.get_client_email(file_number)
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            
            else:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Unknown tool: {name}"
                    })
                )]
    
    async def run(self):
        """Run the MCP server"""
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    config.validate()
    server = DebtCollectionMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())