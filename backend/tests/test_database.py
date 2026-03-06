import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Conversation, KnowledgeUpdate, QueryPattern

@pytest.fixture
def db_session():
    """Create in-memory database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_conversation(db_session):
    """Test creating a conversation"""
    conv = Conversation(
        user_id="test_user",
        messages=[{"role": "user", "content": "Hello"}],
        conversation_metadata={"topic": "greeting"}
    )
    db_session.add(conv)
    db_session.commit()

    assert conv.id is not None
    assert conv.user_id == "test_user"
    assert len(conv.messages) == 1

def test_create_knowledge_update(db_session):
    """Test creating a knowledge update"""
    update = KnowledgeUpdate(
        source="github/CHULOOPA/README.md",
        content="New content",
        diff="+ Added new line",
        status="pending"
    )
    db_session.add(update)
    db_session.commit()

    assert update.id is not None
    assert update.status == "pending"

def test_create_query_pattern(db_session):
    """Test creating a query pattern"""
    pattern = QueryPattern(
        question_type="experience",
        count=5
    )
    db_session.add(pattern)
    db_session.commit()

    assert pattern.id is not None
    assert pattern.count == 5
