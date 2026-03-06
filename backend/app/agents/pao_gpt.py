"""Main pao-gpt agent orchestrator"""
from typing import List, Dict
from app.agents.chains.guard_chain import GuardChain
from app.agents.chains.rag_chain import RAGChain


class PaoGPT:
    """
    Main agent that orchestrates:
    1. Guard chain (safety checks)
    2. RAG chain (retrieval + generation)
    3. Response filtering
    """

    def __init__(self):
        self.guard = GuardChain()
        self.rag = RAGChain()

    async def chat(
        self,
        query: str,
        conversation_id: str = None,
        history: List[Dict] = None
    ) -> Dict:
        """
        Process user message and return response

        Args:
            query: User message
            conversation_id: Optional conversation ID for tracking
            history: Conversation history (list of {role, content} dicts)

        Returns: {
            "response": str,
            "conversation_id": str,
            "blocked": bool,
            "reason": str | None
        }
        """
        # Default history to empty list
        if history is None:
            history = []

        # 1. Guard check
        guard_result = self.guard.check(query)
        if guard_result.is_malicious:
            return {
                "response": guard_result.response,
                "conversation_id": conversation_id,
                "blocked": True,
                "reason": guard_result.reason
            }

        # 2. Retrieve relevant context (full-context approach)
        context = await self.rag.retrieve(query)

        # 3. Generate response with personality
        response = await self.rag.generate(
            query=query,
            context=context,
            history=history
        )

        # 4. Filter response for sensitive info
        filtered_response = self.guard.filter_response(response)

        return {
            "response": filtered_response,
            "conversation_id": conversation_id,
            "blocked": False,
            "reason": None
        }


# Global instance
_agent = None


def get_agent() -> PaoGPT:
    """Get or create agent singleton"""
    global _agent
    if _agent is None:
        _agent = PaoGPT()
    return _agent
