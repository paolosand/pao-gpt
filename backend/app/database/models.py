from sqlalchemy import Column, String, Text, Integer, TIMESTAMP, JSON, TypeDecorator, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

# UUID type that works with both PostgreSQL and SQLite
class UUID(TypeDecorator):
    """Platform-independent UUID type.
    Uses PostgreSQL's UUID type, otherwise uses String(36)
    """
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                try:
                    return str(uuid.UUID(value))
                except ValueError as e:
                    raise ValueError(f"Invalid UUID string: {value}") from e
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value

Base = declarative_base()

class Conversation(Base):
    """Conversation storage for analytics"""
    __tablename__ = "conversations"
    __table_args__ = (
        Index('ix_conversations_user_id', 'user_id'),
        Index('ix_conversations_created_at', 'created_at'),
    )

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(64), nullable=True)  # Anonymous hash
    messages = Column(JSON, nullable=False)  # [{role, content, timestamp}]
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    conversation_metadata = Column(JSON, nullable=True)  # Topic tags, sentiment

class KnowledgeUpdate(Base):
    """Knowledge update approval queue"""
    __tablename__ = "knowledge_updates"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name='valid_status'
        ),
        Index('ix_knowledge_updates_status', 'status'),
        Index('ix_knowledge_updates_created_at', 'created_at'),
    )

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    source = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    diff = Column(Text, nullable=True)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    created_at = Column(TIMESTAMP, server_default=func.now())

class QueryPattern(Base):
    """Analytics aggregations"""
    __tablename__ = "query_patterns"
    __table_args__ = (
        Index('ix_query_patterns_question_type', 'question_type'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_type = Column(String(100), nullable=False)  # experience, project, music
    count = Column(Integer, default=0)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
