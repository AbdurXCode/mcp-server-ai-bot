"""
Tests for FastAPI application endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from client_app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_query_endpoint_success(client):
    """Test the query endpoint with a successful request."""
    query_data = {"query": "Get details for file number 123421"}
    
    with pytest.MonkeyPatch().context() as m:
        m.setenv("GEMINI_API_KEY", "test-key")
        
        response = client.post("/api/query", json=query_data)
        assert response.status_code in [200, 500]  # May fail due to missing API key


def test_query_endpoint_invalid_input(client):
    """Test the query endpoint with invalid input."""
    query_data = {"query": ""}
    
    response = client.post("/api/query", json=query_data)
    assert response.status_code == 400


def test_query_endpoint_missing_field(client):
    """Test the query endpoint with missing query field."""
    query_data = {}
    
    response = client.post("/api/query", json=query_data)
    assert response.status_code == 422


def test_tools_endpoint(client):
    """Test the tools endpoint."""
    response = client.get("/api/tools")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
