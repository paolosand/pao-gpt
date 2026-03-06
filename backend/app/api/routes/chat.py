"""Chat API endpoint"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.agents.pao_gpt import get_agent
from app.database.session import get_db_dependency
from app.database.repositories.conversation_repo import ConversationRepository
from app.config import settings

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request model"""
    query: str = Field(..., min_length=1, max_length=2000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID")
    user_id: Optional[str] = Field(None, description="Optional user ID")


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    blocked: Optional[bool] = Field(False, description="Whether message was blocked")
    reason: Optional[str] = Field(None, description="Reason for blocking")


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db_dependency)
):
    """
    Chat with pao-gpt

    - Checks message with guard chain
    - Retrieves relevant context from knowledge base
    - Generates response with personality
    - Stores conversation for analytics (if enabled in settings)
    """
    agent = get_agent()
    repo = ConversationRepository(db)

    # Get or create conversation
    conversation_history = []
    conversation_id = request.conversation_id

    if conversation_id:
        conv = repo.get_conversation(conversation_id)
        if conv:
            conversation_history = conv.messages
        else:
            # Invalid conversation ID - return error
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation if storage is enabled
        if settings.enable_conversation_storage:
            conv = repo.create_conversation(user_id=request.user_id)
            conversation_id = str(conv.id)

    # Get response from agent
    result = await agent.chat(
        query=request.query,
        conversation_id=conversation_id,
        history=conversation_history
    )

    # Add user message and agent response to history
    if settings.enable_conversation_storage and conversation_id:
        conversation_history.append({
            "role": "user",
            "content": request.query,
            "timestamp": datetime.utcnow().isoformat()
        })
        conversation_history.append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.utcnow().isoformat()
        })

        # Update conversation in database
        repo.update_conversation(conversation_id, conversation_history)

    return ChatResponse(
        response=result["response"],
        conversation_id=conversation_id or "none",
        blocked=result.get("blocked", False),
        reason=result.get("reason")
    )
