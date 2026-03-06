"""RAG chain for retrieval and generation"""
import logging
from typing import List, Dict
from app.services.llm import get_llm
from app.services.knowledge_loader import load_all_knowledge
from app.agents.chains.personality import SYSTEM_PROMPT

MAX_QUERY_LENGTH = 1000

class RAGChain:
    """
    Retrieval Augmented Generation chain
    1. Load all knowledge base documents (full-context prompting)
    2. Generate response with full context + history

    Note: Using full-context approach instead of vector search because:
    - Knowledge base is small (~2k tokens vs 1M context window)
    - Eliminates retrieval ranking issues
    - Simpler and more reliable for portfolio-sized datasets
    """

    def __init__(self):
        self.llm = get_llm()

    async def retrieve(self, query: str) -> List[Dict]:
        """
        Load all knowledge base documents for full-context prompting.

        Returns: List of {content, metadata} dicts containing all portfolio knowledge

        Note: No filtering/ranking needed - knowledge base is small enough (~2k tokens)
        to pass everything to the LLM every time.
        """
        # Load all documents from knowledge base
        return load_all_knowledge()

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
