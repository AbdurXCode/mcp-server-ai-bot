"""Configuration management for MCP Server"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        # API Configuration
        self.api_key: Optional[str] = os.getenv("API_KEY")
        self.api_url: str = os.getenv("API_URL", "https://newip.collectco.com/emilyai")
        self.api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))
        
        # LLM Configuration
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        
        # Server Configuration
        self.server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
        self.server_port: int = int(os.getenv("SERVER_PORT", "8000"))
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"
        
        # MCP Configuration
        self.mcp_server_name: str = os.getenv("MCP_SERVER_NAME", "company-mcp-server")
        self.mcp_server_version: str = os.getenv("MCP_SERVER_VERSION", "1.0.0")
    
    def validate(self) -> bool:
        """Validate that required settings are present"""
        if not self.api_key:
            raise ValueError("API_KEY must be set in environment variables")
        return True
    
    def validate_llm(self) -> bool:
        """Validate LLM-specific settings"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment variables")
        return True


# Global settings instance
settings = Settings()

