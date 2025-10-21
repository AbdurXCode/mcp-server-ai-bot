# Contributing to MCP LLM Server

First off, thank you for considering contributing to MCP LLM Server! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

**When submitting a bug report, include:**

- Clear and descriptive title
- Detailed steps to reproduce the issue
- Expected behavior vs actual behavior
- Screenshots (if applicable)
- Your environment details (OS, Python version, etc.)
- Relevant logs or error messages

**Example:**

```markdown
**Bug Description**: Server crashes when invalid file number is provided

**Steps to Reproduce**:
1. Start the server with `uvicorn app.main:app --reload`
2. Send POST request to `/test/get_user_details` with `{"file_number": "invalid"}`
3. Server returns 500 error

**Expected Behavior**: Should return graceful error message with 400 status

**Environment**:
- OS: Windows 11
- Python: 3.11.2
- FastAPI: 0.109.0
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- Clear and descriptive title
- Detailed description of the proposed enhancement
- Explanation of why this enhancement would be useful
- Possible implementation approaches (if you have ideas)

### Pull Requests

- Fill in the required template
- Follow the coding standards
- Include appropriate test coverage
- Update documentation as needed
- Ensure all tests pass

## 🛠️ Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv)

### Setup Steps

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-llm-server.git
   cd mcp-llm-server
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Verify setup**
   - Open http://localhost:8000/docs
   - Test the health check endpoint

## 🔄 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise code
   - Follow the coding standards
   - Add comments where necessary
   - Update documentation

3. **Test your changes**
   ```bash
   # Run the server and test manually
   uvicorn app.main:app --reload
   
   # Test all endpoints
   # Verify no errors in logs
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Fill in the PR template
   - Wait for review

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if applicable)
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] PR description clearly describes the changes

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Use double quotes for strings
- **Imports**: Group in this order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

### Example Code Style

```python
"""Module docstring describing the purpose"""

import os
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.tools.user_tools import user_tools


class ExampleClass:
    """Class docstring describing the class"""
    
    def __init__(self, param: str):
        """Initialize with parameter"""
        self.param = param
    
    def example_method(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Method docstring describing what it does.
        
        Args:
            input_data: Description of input parameter
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: Description of when this is raised
        """
        if not input_data:
            raise ValueError("Input data cannot be empty")
        
        # Process data
        result = self._process_data(input_data)
        return result
    
    def _process_data(self, data: Dict[str, Any]) -> str:
        """Private method for internal processing"""
        return str(data)


# Constants should be uppercase
API_VERSION = "1.0.0"
MAX_RETRIES = 3
```

### Documentation

- All modules should have docstrings
- All classes should have docstrings
- All public methods should have docstrings
- Complex logic should have inline comments
- Update README.md for significant changes

### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional, Any

def process_data(
    items: List[str],
    config: Dict[str, Any],
    timeout: Optional[int] = None
) -> Dict[str, Any]:
    """Process items with configuration"""
    pass
```

## 📬 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Feature
feat(llm): add support for GPT-4 model

# Bug fix
fix(api): handle null file_number in user_tools

# Documentation
docs(readme): update installation instructions

# Refactor
refactor(agent): simplify prompt generation logic

# Multiple lines
feat(api): add batch processing endpoint

Add new endpoint for processing multiple file numbers at once.
This improves performance for bulk operations.

Closes #123
```

### Scope

Common scopes:
- `api` - API endpoints
- `llm` - LLM agent functionality
- `mcp` - MCP server functionality
- `config` - Configuration management
- `docs` - Documentation
- `ui` - Web interface

## 🧪 Testing Guidelines

### Manual Testing

Before submitting a PR, test:

1. **All API endpoints**
   - Health check
   - MCP tools
   - LLM chat
   - AI summarization

2. **Error handling**
   - Invalid inputs
   - Missing API keys
   - Network failures

3. **Web interface**
   - All buttons work
   - Responses display correctly
   - No console errors

### Testing Checklist

- [ ] Server starts without errors
- [ ] All endpoints return expected responses
- [ ] Error messages are user-friendly
- [ ] No sensitive data in logs
- [ ] Performance is acceptable
- [ ] UI is responsive

## 🎨 Adding New Features

### Adding a New MCP Tool

1. **Define the tool** in `app/tools/user_tools.py`:
   ```python
   async def get_payment_history(self, file_number: str) -> Dict[str, Any]:
       """Get payment history for a file number"""
       # Implementation
   ```

2. **Register in MCP server** in `app/server.py`:
   ```python
   Tool(
       name="get_payment_history",
       description="Retrieves payment history...",
       inputSchema={...}
   )
   ```

3. **Add handler** in `app/server.py`:
   ```python
   if name == "get_payment_history":
       result = await user_tools.get_payment_history(arguments["file_number"])
   ```

4. **Add endpoint** in `app/main.py` (if needed)

5. **Update documentation**

### Adding a New LLM Feature

1. **Add method** to `LLMAgent` class in `app/llm_agent.py`
2. **Create endpoint** in `app/main.py`
3. **Update web interface** if needed
4. **Document** in README.md

## 💬 Questions?

Feel free to:
- Open an issue with the `question` label
- Start a discussion in GitHub Discussions
- Contact the maintainers

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! ❤️

---

**Happy Coding!** 🚀

