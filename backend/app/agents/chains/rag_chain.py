"""RAG chain for retrieval and generation"""
from typing import List, Dict
from app.services.llm import get_llm
from app.agents.chains.personality import SYSTEM_PROMPT

class RAGChain:
    """
    Retrieval Augmented Generation chain
    1. Retrieve relevant context from vector store
    2. Generate response with context + history
    """

    def __init__(self, vector_store=None):
        self.vector_store = vector_store
        self.llm = get_llm()

    async def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve relevant documents from vector store
        Returns: List of {content, metadata} dicts
        """
        if self.vector_store is None:
            # Stub: Return empty context for now
            return []

        # TODO: Implement after ChromaDB setup in Task 4
        # results = self.vector_store.similarity_search(query, k=5)
        # return results
        return []

    async def generate(self, query: str, context: List[Dict], history: List[Dict]) -> str:
        """
        Generate response using context and conversation history
        """
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
