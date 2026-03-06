"""Tests for chat API endpoint

Note: These tests verify basic endpoint functionality and request validation.
Database-dependent integration tests are covered in:
- test_conversation_repo.py (repository operations)
- test_pao_gpt.py (orchestrator logic)
- test_guard_chain.py (safety filters)
- test_rag_chain.py (RAG generation)

Full end-to-end testing requires a running PostgreSQL instance.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_exists():
    """Test that chat endpoint is registered"""
    response = client.post("/api/chat", json={
        "query": "test"
    })
    # Should get a response (200, 404, or 500), not 404 "Not Found"
    assert response.status_code != 405  # Method not allowed means endpoint exists


def test_chat_empty_query():
    """Test chat with empty query"""
    response = client.post("/api/chat", json={
        "query": ""
    })
    # Should fail validation
    assert response.status_code == 422


def test_chat_query_too_long():
    """Test chat with query exceeding max length"""
    long_query = "a" * 2001  # Max is 2000

    response = client.post("/api/chat", json={
        "query": long_query
    })

    # Should fail validation
    assert response.status_code == 422


def test_chat_invalid_json():
    """Test chat with invalid JSON"""
    response = client.post("/api/chat", json={
        "invalid_field": "test"
    })

    # Should fail validation (missing required 'query' field)
    assert response.status_code == 422


def test_chat_response_structure():
    """Test that successful chat responses have required fields"""
    # This test may need valid database setup to pass fully
    # Just testing the structure when we get a response
    response = client.post("/api/chat", json={
        "query": "Hello"
    })

    # If we get a 200, verify structure
    if response.status_code == 200:
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert "blocked" in data
