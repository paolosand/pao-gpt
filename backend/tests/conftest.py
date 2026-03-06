import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
def test_settings():
    """Override settings for testing"""
    from app.config import Settings
    return Settings(
        google_api_key="test_key",
        admin_key="test_admin",
        database_url="postgresql://test:test@localhost:5432/test",
        environment="test"
    )
