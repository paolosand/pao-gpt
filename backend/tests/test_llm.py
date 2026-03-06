"""Tests for LLM service"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.llm import get_llm

def test_get_llm_returns_correct_model():
    """Test that get_llm returns ChatGoogleGenerativeAI with correct config"""
    with patch('app.services.llm.ChatGoogleGenerativeAI') as mock_llm:
        mock_instance = MagicMock()
        mock_llm.return_value = mock_instance

        llm = get_llm()

        # Verify LLM was instantiated with correct parameters
        mock_llm.assert_called_once()
        call_kwargs = mock_llm.call_args.kwargs

        assert call_kwargs['model'] == "gemini-1.5-flash"
        assert call_kwargs['temperature'] == 0.7
        assert call_kwargs['max_output_tokens'] == 1024
        assert 'google_api_key' in call_kwargs

def test_get_llm_uses_settings_api_key():
    """Test that get_llm uses API key from settings"""
    with patch('app.services.llm.settings') as mock_settings:
        mock_settings.google_api_key = "test_api_key_12345"

        with patch('app.services.llm.ChatGoogleGenerativeAI') as mock_llm:
            get_llm()

            call_kwargs = mock_llm.call_args.kwargs
            assert call_kwargs['google_api_key'] == "test_api_key_12345"
