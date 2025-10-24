#!/usr/bin/env python3
"""
Run script for the Debt Collection MCP Application
"""

import sys
import os
import uvicorn

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from client_app.main import app
from mcp_server.config import config

if __name__ == "__main__":
    try:
        # Validate configuration
        config.validate()
        
        print("Starting Debt Collection MCP Application...")
        print(f"Server will be available at: http://{config.FASTAPI_HOST}:{config.FASTAPI_PORT}")
        print("Press Ctrl+C to stop the server")
        
        # Run the application
        uvicorn.run(
            "client_app.main:app",
            host=config.FASTAPI_HOST,
            port=config.FASTAPI_PORT,
            reload=True
        )
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        print("See SETUP.md for configuration instructions.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
