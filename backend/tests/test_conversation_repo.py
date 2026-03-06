"""Tests for conversation repository"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Conversation
from app.database.repositories.conversation_repo import ConversationRepository


@pytest.fixture
def db_session():
    """Create in-memory database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def repo(db_session):
    """Create conversation repository"""
    return ConversationRepository(db_session)


def test_create_conversation(repo):
    """Test creating a conversation"""
    conv = repo.create_conversation(user_id="test_user")

    assert conv.id is not None
    assert conv.user_id == "test_user"
    assert conv.messages == []
    assert conv.conversation_metadata == {}


def test_get_conversation(repo):
    """Test getting a conversation by ID"""
    # Create conversation
    conv = repo.create_conversation(user_id="test_user")
    conv_id = str(conv.id)

    # Get conversation
    retrieved = repo.get_conversation(conv_id)

    assert retrieved is not None
    assert str(retrieved.id) == conv_id
    assert retrieved.user_id == "test_user"


def test_get_conversation_not_found(repo):
    """Test getting a non-existent conversation"""
    result = repo.get_conversation("00000000-0000-0000-0000-000000000000")
    assert result is None


def test_get_conversation_invalid_id(repo):
    """Test getting conversation with invalid ID"""
    result = repo.get_conversation("not-a-uuid")
    assert result is None


def test_update_conversation(repo):
    """Test updating conversation messages"""
    # Create conversation
    conv = repo.create_conversation(user_id="test_user")
    conv_id = str(conv.id)

    # Update messages
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    updated = repo.update_conversation(conv_id, messages)

    assert updated is not None
    assert len(updated.messages) == 2
    assert updated.messages[0]["role"] == "user"
    assert updated.messages[1]["role"] == "assistant"


def test_update_conversation_not_found(repo):
    """Test updating a non-existent conversation"""
    result = repo.update_conversation(
        "00000000-0000-0000-0000-000000000000",
        [{"role": "user", "content": "Hello"}]
    )
    assert result is None


def test_list_conversations(repo):
    """Test listing conversations for a user"""
    # Create multiple conversations
    repo.create_conversation(user_id="user1")
    repo.create_conversation(user_id="user1")
    repo.create_conversation(user_id="user2")

    # List conversations for user1
    conversations = repo.list_conversations("user1", limit=10)

    assert len(conversations) == 2
    assert all(conv.user_id == "user1" for conv in conversations)


def test_list_conversations_limit(repo):
    """Test listing conversations with limit"""
    # Create multiple conversations
    for _ in range(5):
        repo.create_conversation(user_id="user1")

    # List with limit
    conversations = repo.list_conversations("user1", limit=3)

    assert len(conversations) == 3
