import pytest
from app.agents.chains.rag_chain import RAGChain

@pytest.mark.asyncio
async def test_rag_chain_validates_empty_query():
    """Test that empty queries are rejected"""
    rag = RAGChain()
    response = await rag.generate("", [], [])
    assert "provide a question" in response.lower()

@pytest.mark.asyncio
async def test_rag_chain_validates_long_query():
    """Test that overly long queries are rejected"""
    rag = RAGChain()
    long_query = "a" * 1001
    response = await rag.generate(long_query, [], [])
    assert "too long" in response.lower()

@pytest.mark.asyncio
async def test_format_context():
    """Test context formatting"""
    rag = RAGChain()
    context = [
        {"content": "Paolo works at Nuts and Bolts AI", "metadata": {"source": "experience.md"}},
        {"content": "He studied at CalArts", "metadata": {"source": "education.md"}}
    ]
    formatted = rag._format_context(context)
    assert "Paolo works at Nuts and Bolts AI" in formatted
    assert "source:" in formatted.lower()

@pytest.mark.asyncio
async def test_format_history():
    """Test history formatting"""
    rag = RAGChain()
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"}
    ]
    formatted = rag._format_history(history)
    assert "USER: Hi" in formatted
    assert "ASSISTANT: Hello!" in formatted

@pytest.mark.asyncio
async def test_retrieve_loads_all_knowledge():
    """Test that retrieve loads all knowledge base documents"""
    rag = RAGChain()
    docs = await rag.retrieve("test query")
    # Should load all 4 markdown files
    assert len(docs) >= 4
    doc_types = [d['metadata']['type'] for d in docs]
    assert 'experience' in doc_types
    assert 'education' in doc_types
    assert 'projects' in doc_types
    assert 'skills' in doc_types
