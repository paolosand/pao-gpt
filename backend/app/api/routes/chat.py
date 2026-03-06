"""Chat API endpoint"""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.agents.pao_gpt import get_agent
from app.database.session import get_db_dependency
from app.database.repositories.conversation_repo import ConversationRepository
from app.config import settings

router = APIRouter(tags=["chat"])
limiter = Limiter(key_func=get_remote_address)

# Configure logging
logging.basicConfig(level=logging.INFO)


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
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(
    chat_request: ChatRequest,
    request: Request,
    db: Session = Depends(get_db_dependency)
):
    """
    Chat with pao-gpt

    - Checks message with guard chain
    - Retrieves relevant context from knowledge base
    - Generates response with personality
    - Stores conversation for analytics (if enabled in settings)
    """
    try:
        agent = get_agent()
        repo = ConversationRepository(db)

        # Get or create conversation
        conversation_history = []
        conversation_id = chat_request.conversation_id

        if conversation_id:
            try:
                conv = repo.get_conversation(conversation_id)
                if conv:
                    conversation_history = conv.messages
                else:
                    # Invalid conversation ID - return error
                    raise HTTPException(status_code=404, detail="Conversation not found")
            except HTTPException:
                raise
            except Exception as e:
                logging.error(f"Database error retrieving conversation: {e}")
                raise HTTPException(status_code=500, detail="Error accessing conversation")
        else:
            # Create new conversation if storage is enabled
            if settings.enable_conversation_storage:
                try:
                    conv = repo.create_conversation(user_id=chat_request.user_id)
                    conversation_id = str(conv.id)
                except Exception as e:
                    logging.error(f"Database error creating conversation: {e}")
                    raise HTTPException(status_code=500, detail="Error creating conversation")

        # Get response from agent
        try:
            result = await agent.chat(
                query=chat_request.query,
                conversation_id=conversation_id,
                history=conversation_history
            )
        except Exception as e:
            logging.error(f"Agent error: {e}")
            raise HTTPException(status_code=500, detail="Error generating response")

        # Add user message and agent response to history
        if settings.enable_conversation_storage and conversation_id:
            conversation_history.append({
                "role": "user",
                "content": chat_request.query,
                "timestamp": datetime.utcnow().isoformat()
            })
            conversation_history.append({
                "role": "assistant",
                "content": result["response"],
                "timestamp": datetime.utcnow().isoformat()
            })

            # Update conversation in database
            try:
                repo.update_conversation(conversation_id, conversation_history)
            except Exception as e:
                logging.error(f"Database error updating conversation: {e}")
                # Don't fail the request if we can't save history
                pass

        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id or "none",
            blocked=result.get("blocked", False),
            reason=result.get("reason")
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logging.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
