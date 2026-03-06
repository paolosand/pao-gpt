"""Gemini Flash LLM client"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def get_llm():
    """Get Gemini Flash LLM instance"""
    return ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        google_api_key=settings.google_api_key,
        temperature=0.7,
        max_output_tokens=1024,
    )
