import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for MCP Server"""
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # MCP Server Configuration
    MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 5000))
    
    # FastAPI Configuration
    FASTAPI_HOST = os.getenv("FASTAPI_HOST", "localhost")
    FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))
    
    # External API Configuration
    DEBT_COLLECTION_API_URL = os.getenv(
        "DEBT_COLLECTION_API_URL",
        "https://your-api-endpoint.com/api/user-details"
    )
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 20))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required in .env file")
        return True

config = Config()