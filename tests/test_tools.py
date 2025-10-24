"""
Tests for MCP tools functionality.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from mcp_server.tools import DebtCollectionTools


class TestDebtCollectionTools:
    """Test cases for DebtCollectionTools class."""

    @pytest.fixture
    def tools(self):
        """Create a DebtCollectionTools instance for testing."""
        return DebtCollectionTools()

    @pytest.mark.asyncio
    async def test_get_user_details_by_file_number_success(self, tools):
        """Test successful retrieval of user details."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "file_number": "123421",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "status": "active"
        }
        mock_response.status_code = 200
        
        with patch('requests.get', return_value=mock_response):
            result = await tools.get_user_details_by_file_number("123421")
            
            assert result["file_number"] == "123421"
            assert result["name"] == "John Doe"
            assert result["email"] == "john.doe@example.com"

    @pytest.mark.asyncio
    async def test_get_user_details_by_file_number_invalid_input(self, tools):
        """Test handling of invalid file number."""
        with pytest.raises(ValueError, match="File number cannot be empty"):
            await tools.get_user_details_by_file_number("")

    @pytest.mark.asyncio
    async def test_get_user_details_by_file_number_api_error(self, tools):
        """Test handling of API errors."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "File not found"}
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(Exception, match="API request failed"):
                await tools.get_user_details_by_file_number("123421")

    @pytest.mark.asyncio
    async def test_get_client_email_success(self, tools):
        """Test successful email extraction."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "file_number": "123421",
            "email": "john.doe@example.com"
        }
        mock_response.status_code = 200
        
        with patch('requests.get', return_value=mock_response):
            result = await tools.get_client_email("123421")
            
            assert result == "john.doe@example.com"

    @pytest.mark.asyncio
    async def test_get_client_email_no_email(self, tools):
        """Test handling when email is not available."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "file_number": "123421",
            "name": "John Doe"
        }
        mock_response.status_code = 200
        
        with patch('requests.get', return_value=mock_response):
            result = await tools.get_client_email("123421")
            
            assert result == "Email not available"
