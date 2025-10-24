from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client_app.mcp_client import MCPClient
from mcp_server.config import config


app = FastAPI(title="Debt Collection MCP Application")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="client_app/templates")

# Initialize MCP Client
mcp_client = MCPClient()


class QueryRequest(BaseModel):
    query: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/query")
async def process_query(request: QueryRequest):
    """Process user query through MCP"""
    result = await mcp_client.process_query(request.query)
    return result


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mcp_server": "connected",
        "gemini": "configured"
    }


@app.get("/api/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": mcp_client.tool_definitions
    }


if __name__ == "__main__":
    config.validate()
    print("Starting Debt Collection MCP Application...")
    print(f"Server will be available at: http://{config.FASTAPI_HOST}:{config.FASTAPI_PORT}")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host=config.FASTAPI_HOST,
        port=config.FASTAPI_PORT,
        reload=False
    )