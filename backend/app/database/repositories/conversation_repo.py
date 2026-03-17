"""Conversation repository for database operations"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.database.models import Conversation
import uuid


class ConversationRepository:
    """CRUD operations for conversations"""

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: Optional[str] = None) -> Conversation:
        """Create new conversation with empty messages"""
        conv = Conversation(
            user_id=user_id,
            messages=[],
            conversation_metadata={}
        )
        self.db.add(conv)
        self.db.flush()  # Get ID without committing
        return conv

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        try:
            conv_uuid = uuid.UUID(conversation_id)
            return self.db.query(Conversation).filter(Conversation.id == conv_uuid).first()
        except (ValueError, AttributeError):
            return None

    def update_conversation(self, conversation_id: str, messages: List[Dict]) -> Optional[Conversation]:
        """Update conversation messages"""
        conv = self.get_conversation(conversation_id)
        if conv:
            conv.messages = messages
            flag_modified(conv, 'messages')
            self.db.flush()
        return conv

    def list_conversations(self, user_id: str, limit: int = 10) -> List[Conversation]:
        """List conversations for a user"""
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )
