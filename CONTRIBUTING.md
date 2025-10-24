# Contributing to Debt Collection MCP

Thank you for your interest in contributing to the Debt Collection MCP project! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account
- Basic knowledge of FastAPI, MCP, and Python

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/debt-collection-mcp.git
   cd debt-collection-mcp
   ```

3. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/originalowner/debt-collection-mcp.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

6. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

## 🔄 Contributing Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bugfix-name
# or
git checkout -b docs/your-docs-update
```

### 2. Make Changes

- Write clean, readable code
- Follow the coding standards
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
pytest

# Run linting
flake8 .

# Run type checking
mypy .

# Run security checks
bandit -r .
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📏 Coding Standards

### Python Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Example:

```python
async def get_user_details_by_file_number(self, file_number: str) -> Dict[str, Any]:
    """
    Retrieve user details by file number.
    
    Args:
        file_number: The file number to search for
        
    Returns:
        Dictionary containing user details
        
    Raises:
        ValueError: If file_number is invalid
        APIError: If API request fails
    """
    if not file_number or not file_number.strip():
        raise ValueError("File number cannot be empty")
    
    # Implementation here
    pass
```

### File Organization

- Keep related functionality together
- Use clear module names
- Separate concerns (API, business logic, data access)

## 🧪 Testing

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

### Example:

```python
import pytest
from unittest.mock import Mock, patch
from mcp_server.tools import DebtCollectionTools

@pytest.mark.asyncio
async def test_get_user_details_by_file_number_success():
    """Test successful retrieval of user details."""
    tools = DebtCollectionTools()
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"file_number": "123", "name": "John Doe"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = await tools.get_user_details_by_file_number("123")
        
        assert result["file_number"] == "123"
        assert result["name"] == "John Doe"

@pytest.mark.asyncio
async def test_get_user_details_by_file_number_invalid_input():
    """Test handling of invalid file number."""
    tools = DebtCollectionTools()
    
    with pytest.raises(ValueError, match="File number cannot be empty"):
        await tools.get_user_details_by_file_number("")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run with verbose output
pytest -v
```

## 📚 Documentation

### Code Documentation

- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Include examples in docstrings where helpful

### README Updates

- Update README.md when adding new features
- Include usage examples
- Update installation instructions if needed

### API Documentation

- Update API endpoint documentation
- Include request/response examples
- Document error codes and messages

## 🐛 Issue Reporting

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check if the issue is already fixed in the latest version
3. Ensure you can reproduce the issue

### Creating a Good Issue

Use the issue template and include:

- **Clear title**: Brief description of the issue
- **Description**: Detailed explanation of the problem
- **Steps to reproduce**: Exact steps to reproduce the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, etc.
- **Screenshots**: If applicable

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed

## 🔀 Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/your-feature-name
   git rebase main
   ```

2. **Run all checks**
   ```bash
   pytest
   flake8 .
   mypy .
   bandit -r .
   ```

3. **Update documentation** if needed

### PR Template

Fill out the PR template with:

- **Description**: What changes were made and why
- **Type of change**: Bug fix, new feature, documentation, etc.
- **Testing**: How was it tested
- **Checklist**: Confirm all items are completed

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in staging environment
4. **Approval** by at least one maintainer

### After Approval

- Maintainers will merge the PR
- Delete the feature branch
- Celebrate your contribution! 🎉

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- `1.0.0` for initial release
- `1.1.0` for new features
- `1.0.1` for bug fixes

### Creating a Release

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create a release tag
4. GitHub Actions will handle the rest

## 🤝 Community

### Getting Help

- **GitHub Discussions**: For questions and general discussion
- **Issues**: For bug reports and feature requests
- **Discord/Slack**: For real-time chat (if available)

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Annual contributor appreciation

## 📝 Additional Resources

- [Python Style Guide](https://pep8.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 🙏 Thank You

Thank you for contributing to the Debt Collection MCP project! Your contributions help make this project better for everyone.

---

**Questions?** Feel free to open an issue or start a discussion!
