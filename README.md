# 🤖 AI Assistant Platform

A Model Context Protocol (MCP) server integrated with Google Gemini LLM for intelligent customer service assistance. This platform provides natural language chat capabilities and AI-powered customer data analysis and summarization.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **🔧 MCP Tool Integration**: Standardized tool interface following Model Context Protocol
- **🤖 AI-Powered Chat**: Natural language interaction using Google Gemini 1.5 Flash
- **📊 Smart Analytics**: AI-generated customer insights and summaries
- **🔒 Secure API**: Bearer token authentication for external API calls
- **🌐 Professional Web Interface**: Modern UI for customer service operations
- **📖 Auto-Generated Docs**: FastAPI automatic API documentation

## 📁 Project Structure

```
ai-assistant-platform/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── server.py               # MCP server setup
│   ├── llm_agent.py            # Gemini LLM integration
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration management
│   ├── tools/
│   │   ├── __init__.py
│   │   └── user_tools.py       # MCP tools implementation
│   └── static/
│       └── index.html          # Web interface
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- External API credentials (for customer data integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-assistant-platform.git
   cd ai-assistant-platform
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual credentials
   # On Windows: notepad .env
   # On Linux/Mac: nano .env
   ```
   
   Required environment variables:
   ```env
   API_KEY=your_api_key_here
   API_URL=https://your-api-url.com
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the server**
   ```bash
   # Using uvicorn directly
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
   # OR using Python module
   python -m app.main
   ```

6. **Access the application**
   - 🏠 Home/Health Check: http://localhost:8000/
   - 📖 API Documentation: http://localhost:8000/docs
   - 🌐 Web Interface: http://localhost:8000/ui
   - 🔧 List Tools: http://localhost:8000/tools

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/ui` | Web interface |
| GET | `/tools` | List available MCP tools |
| GET | `/config` | View current configuration |
| GET | `/docs` | Interactive API documentation |

### MCP Tool Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/test/get_user_details` | Test MCP tool with file number |

**Request Body:**
```json
{
  "file_number": "ABC123"
}
```

### LLM Endpoints

#### Chat with LLM
`POST /llm/chat`

Natural language chat with optional customer context.

**Request Body:**
```json
{
  "message": "What's my current balance?",
  "file_number": "ABC123"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "response": "Based on your account, your current balance is $1,500.00..."
}
```

#### AI Summary
`POST /llm/summarize`

Generate AI-powered summary of customer account.

**Request Body:**
```json
{
  "file_number": "ABC123"
}
```

**Response:**
```json
{
  "success": true,
  "summary": "Account Summary for John Doe:\n\nCurrent Balance: $1,500.00..."
}
```

## 🔧 Configuration

All configuration is managed through environment variables in the `.env` file:

```env
# API Configuration
API_KEY=your_api_key_here
API_URL=https://api.example.com
API_TIMEOUT=30

# LLM Configuration
GEMINI_API_KEY=your_gemini_key_here

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=false

# MCP Configuration
MCP_SERVER_NAME=company-mcp-server
MCP_SERVER_VERSION=1.0.0
```

## 🏗️ Architecture

### Data Flow

```
User Request → FastAPI → LLM Agent → MCP Tools → External API
                           ↓
                    Gemini AI Processing
                           ↓
                    AI-Enhanced Response
```

### Components

1. **FastAPI Server** (`main.py`): Handles HTTP requests and routing
2. **LLM Agent** (`llm_agent.py`): Manages Gemini AI interactions
3. **MCP Server** (`server.py`): Implements Model Context Protocol
4. **User Tools** (`user_tools.py`): External API integration
5. **Configuration** (`config.py`): Environment management

## 💡 Usage Examples

### Example 1: Get Customer Details

```python
import requests

response = requests.post(
    "http://localhost:8000/test/get_user_details",
    json={"file_number": "CUST123"}
)
print(response.json())
```

### Example 2: Chat with Context

```python
import requests

response = requests.post(
    "http://localhost:8000/llm/chat",
    json={
        "message": "What payment options are available?",
        "file_number": "CUST123"
    }
)
print(response.json()["response"])
```

### Example 3: Get AI Summary

```python
import requests

response = requests.post(
    "http://localhost:8000/llm/summarize",
    json={"file_number": "CUST123"}
)
print(response.json()["summary"])
```

## 🔌 MCP Client Integration

To use this server with an MCP client (like Claude Desktop):

```json
{
  "mcpServers": {
    "company-mcp-server": {
      "command": "python",
      "args": [
        "/path/to/mcp-llm-server/app/main.py"
      ],
      "env": {
        "API_KEY": "your_api_key_here",
        "GEMINI_API_KEY": "your_gemini_key_here",
        "API_URL": "https://api.example.com"
      }
    }
  }
}
```

## 🧪 Testing

### Using the Web Interface

1. Open http://localhost:8000/ui
2. Enter a file number (default: 14226904)
3. Test different features:
   - MCP Tool Testing
   - LLM Chat
   - AI Summary

### Using curl

```bash
# Test health check
curl http://localhost:8000/

# Test MCP tool
curl -X POST http://localhost:8000/test/get_user_details \
  -H "Content-Type: application/json" \
  -d '{"file_number": "14226904"}'

# Test LLM chat
curl -X POST http://localhost:8000/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the current balance?", "file_number": "14226904"}'
```

## 🛠️ Development

### Adding New MCP Tools

1. **Define the tool in `app/tools/user_tools.py`**:
   ```python
   async def new_tool(self, param: str) -> Dict[str, Any]:
       """Your tool implementation"""
       pass
   ```

2. **Register in `app/server.py`**:
   ```python
   @mcp_server.list_tools()
   async def list_tools() -> list[Tool]:
       return [
           Tool(name="new_tool", description="...", inputSchema={...})
       ]
   ```

3. **Add handler in `app/server.py`**:
   ```python
   @mcp_server.call_tool()
   async def call_tool(name: str, arguments: dict):
       if name == "new_tool":
           result = await user_tools.new_tool(arguments["param"])
   ```

### Running in Development Mode

```bash
# Enable debug mode in .env
DEBUG=true

# Run with auto-reload
uvicorn app.main:app --reload --log-level debug
```

## 📦 Dependencies

- **FastAPI**: Modern web framework for building APIs
- **uvicorn**: ASGI server for FastAPI
- **google-generativeai**: Google Gemini AI SDK
- **httpx**: Async HTTP client for external APIs
- **python-dotenv**: Environment variable management
- **mcp**: Model Context Protocol SDK

See `requirements.txt` for complete list with versions.

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Use HTTPS** in production
5. **Implement rate limiting** for production use
6. **Validate all inputs** before processing
7. **Log security events** for monitoring

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Problem**: `Could not import module "main"`
- **Solution**: Use `uvicorn app.main:app` instead of `uvicorn main:app`

**Problem**: Server not accessible at `http://0.0.0.0:8000`
- **Solution**: Use `http://localhost:8000` or `http://127.0.0.1:8000` in browser

**Problem**: `API_KEY must be set in environment variables`
- **Solution**: Create `.env` file from `.env.example` and fill in your keys

**Problem**: Gemini API errors
- **Solution**: Verify your `GEMINI_API_KEY` is valid and has sufficient quota

## 📞 Support

For issues, questions, or contributions:
- 🐛 Report bugs via GitHub Issues
- 💬 Discussions via GitHub Discussions
- 📧 Email: your.email@example.com

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Google Gemini](https://ai.google.dev/) for LLM capabilities
- [Model Context Protocol](https://github.com/anthropics/mcp) for standardized tool interfaces

---

**Made with ❤️ for intelligent debt collection assistance**
