"""Main entry point for the MCP Server application with FastAPI"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.server import create_server
from app.tools.user_tools import user_tools
from app.llm_agent import llm_agent
from app.core.config import settings
import uvicorn
import os

# Create FastAPI app
app = FastAPI(title="AI Assistant Platform", version="1.0.0", description="Intelligent Customer Service with MCP & LLM Integration")

# Initialize MCP server
mcp_server = create_server()

# Mount static files
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


class FileNumberRequest(BaseModel):
    """Request model for file number lookup"""
    file_number: str


class UserDetailsResponse(BaseModel):
    """Response model for user details"""
    success: bool
    data: dict = None
    error: str = None


class ChatRequest(BaseModel):
    """Request model for LLM chat"""
    message: str
    file_number: str = None


class ChatResponse(BaseModel):
    """Response model for LLM chat"""
    success: bool
    response: str = None
    error: str = None


class SummarizeRequest(BaseModel):
    """Request model for user data summarization"""
    file_number: str


class SummarizeResponse(BaseModel):
    """Response model for user data summarization"""
    success: bool
    summary: str = None
    error: str = None


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "running", "message": "MCP server is live"}


@app.get("/ui")
def serve_ui():
    """Serve the web interface"""
    if os.path.exists("app/static/index.html"):
        return FileResponse("app/static/index.html")
    else:
        return {"message": "Web interface not found. Please check static files."}


@app.get("/tools")
async def list_available_tools():
    """List all available MCP tools"""
    try:
        # Define the tools manually since MCP server doesn't expose them directly
        tools = [
            {
                "name": "get_user_details_by_file_number",
                "description": "Retrieves user details based on the provided file number. This function is used when the AI agent asks the user for their file number and uses it to look up relevant information such as name, contact details, case status, or other associated data.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_number": {
                            "type": "string",
                            "description": "The file number to look up user details"
                        }
                    },
                    "required": ["file_number"]
                }
            }
        ]
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")


@app.post("/test/get_user_details", response_model=UserDetailsResponse)
async def test_get_user_details(request: FileNumberRequest):
    """Test endpoint for get_user_details_by_file_number tool"""
    try:
        # Validate configuration
        settings.validate()
        
        # Call the tool directly
        result = await user_tools.get_user_details_by_file_number(request.file_number)
        
        return UserDetailsResponse(
            success=True,
            data=result
        )
    
    except ValueError as e:
        return UserDetailsResponse(
            success=False,
            error=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        return UserDetailsResponse(
            success=False,
            error=f"API error: {str(e)}"
        )


@app.post("/llm/chat", response_model=ChatResponse)
async def chat_with_llm(request: ChatRequest):
    """Chat with Gemini LLM, optionally using customer data"""
    try:
        # Validate LLM configuration
        settings.validate_llm()
        
        # Get response from LLM agent
        response = llm_agent.chat_with_gemini(
            user_message=request.message,
            file_number=request.file_number
        )
        
        return ChatResponse(
            success=True,
            response=response
        )
    
    except ValueError as e:
        return ChatResponse(
            success=False,
            error=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        return ChatResponse(
            success=False,
            error=f"LLM error: {str(e)}"
        )


@app.post("/llm/summarize", response_model=SummarizeResponse)
async def summarize_user_data(request: SummarizeRequest):
    """Get AI-generated summary of user data"""
    try:
        # Validate LLM configuration
        settings.validate_llm()
        
        # Get summary from LLM agent
        summary = llm_agent.summarize_with_gemini(request.file_number)
        
        return SummarizeResponse(
            success=True,
            summary=summary
        )
    
    except ValueError as e:
        return SummarizeResponse(
            success=False,
            error=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        return SummarizeResponse(
            success=False,
            error=f"LLM error: {str(e)}"
        )


@app.get("/config")
def get_config():
    """Get current configuration (without sensitive data)"""
    return {
        "api_url": settings.api_url,
        "api_timeout": settings.api_timeout,
        "server_host": settings.server_host,
        "server_port": settings.server_port,
        "debug": settings.debug,
        "mcp_server_name": settings.mcp_server_name,
        "mcp_server_version": settings.mcp_server_version,
        "api_key_configured": bool(settings.api_key),
        "gemini_api_key_configured": bool(settings.gemini_api_key)
    }


@app.on_event("startup")
async def start_mcp():
    """Startup event handler"""
    print("✅ AI Assistant Platform started successfully!")
    print(f"🌐 FastAPI server running on http://{settings.server_host}:{settings.server_port}")
    print(f"📋 Available endpoints:")
    print(f"   - GET  / (health check)")
    print(f"   - GET  /ui (web interface)")
    print(f"   - GET  /tools (list MCP tools)")
    print(f"   - POST /test/get_user_details (test MCP tool)")
    print(f"   - POST /llm/chat (chat with Gemini LLM)")
    print(f"   - POST /llm/summarize (AI summary of user data)")
    print(f"   - GET  /config (view configuration)")
    print(f"📖 API docs available at: http://{settings.server_host}:{settings.server_port}/docs")
    print(f"🌐 Web interface available at: http://{settings.server_host}:{settings.server_port}/ui")
    print(f"🤖 LLM Integration: Gemini 1.5 Flash")
    print(f"🔑 API Keys configured: CollectCo={bool(settings.api_key)}, Gemini={bool(settings.gemini_api_key)}")


if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug
    )

