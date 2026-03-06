"""Google Generative AI embedding generation"""
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

def get_embeddings():
    """Get Google Generative AI embeddings instance"""
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.google_api_key
    )
