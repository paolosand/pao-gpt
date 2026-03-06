"""RAG chain for retrieval and generation"""
import logging
from typing import List, Dict
from app.services.llm import get_llm
from app.services.vector_store import get_vector_store
from app.agents.chains.personality import SYSTEM_PROMPT

MAX_QUERY_LENGTH = 1000

class RAGChain:
    """
    Retrieval Augmented Generation chain
    1. Retrieve relevant context from vector store
    2. Generate response with context + history
    """

    def __init__(self, vector_store=None):
        self.vector_store = vector_store or get_vector_store()
        self.llm = get_llm()

    async def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve relevant documents from vector store
        Returns: List of {content, metadata} dicts
        """
        if self.vector_store is None:
            return []

        # Search vector store for relevant context
        results = self.vector_store.similarity_search(query, k=5)
        return results

    async def generate(self, query: str, context: List[Dict], history: List[Dict]) -> str:
        """
        Generate response using context and conversation history
        """
        # Validate input
        if not query or not query.strip():
            return "Please provide a question."

        if len(query) > MAX_QUERY_LENGTH:
            return f"Your question is too long (max {MAX_QUERY_LENGTH} characters). Please shorten it."

        try:
            # Format context
            context_text = self._format_context(context)

            # Format history
            history_text = self._format_history(history)

            # Build prompt
            prompt = f"""{SYSTEM_PROMPT}

CONTEXT FROM KNOWLEDGE BASE:
{context_text if context_text else "No relevant context found."}

CONVERSATION HISTORY:
{history_text if history_text else "No previous messages."}

USER QUESTION: {query}

RESPONSE:"""

            # Generate with LLM
            response = await self.llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            # Log the error
            logging.error(f"LLM generation error: {e}")
            return "I'm having trouble generating a response right now. Could you try rephrasing your question?"

    def _format_context(self, context: List[Dict]) -> str:
        """Format context documents for prompt"""
        if not context:
            return ""

        formatted = []
        for i, doc in enumerate(context, 1):
            source = doc.get("metadata", {}).get("source", "unknown")
            content = doc.get("content", "")
            formatted.append(f"[{i}] Source: {source}\n{content}")

        return "\n\n".join(formatted)

    def _format_history(self, history: List[Dict]) -> str:
        """Format conversation history for prompt"""
        if not history:
            return ""

        formatted = []
        for msg in history[-5:]:  # Last 5 messages only
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.upper()}: {content}")

        return "\n".join(formatted)
