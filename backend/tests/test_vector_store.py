"""Tests for vector store"""
import pytest
import tempfile
import shutil
from pathlib import Path
from app.services.vector_store import VectorStore

@pytest.fixture
def temp_chroma_dir():
    """Create temporary directory for ChromaDB"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_vector_store_initialization(temp_chroma_dir):
    """Test vector store can be initialized"""
    store = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_chroma_dir
    )

    assert store.collection is not None
    assert store.get_collection_count() == 0

def test_vector_store_add_documents(temp_chroma_dir):
    """Test adding documents to vector store"""
    store = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_chroma_dir
    )

    # Add test documents
    documents = [
        {
            'id': 'proj_1',
            'content': 'Project: CHULOOPA - Transformer-based drum generation',
            'metadata': {'type': 'project', 'title': 'CHULOOPA'}
        },
        {
            'id': 'exp_1',
            'content': 'Experience: Built ML pipelines at Stratpoint Technologies from July 2023 to July 2024',
            'metadata': {'type': 'experience', 'company': 'Stratpoint'}
        },
        {
            'id': 'skill_1',
            'content': 'Skill: PyTorch for deep learning and model development',
            'metadata': {'type': 'skill', 'category': 'ML & AI'}
        }
    ]

    store.add_documents(documents)

    # Verify count
    assert store.get_collection_count() == 3

def test_vector_store_similarity_search(temp_chroma_dir):
    """Test similarity search in vector store"""
    store = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_chroma_dir
    )

    # Add test documents
    documents = [
        {
            'id': 'proj_1',
            'content': 'Project: CHULOOPA - Transformer-based drum generation using PyTorch for real-time audio ML',
            'metadata': {'type': 'project', 'title': 'CHULOOPA'}
        },
        {
            'id': 'exp_1',
            'content': 'Experience: Built ML pipelines at Stratpoint Technologies using PyTorch',
            'metadata': {'type': 'experience', 'company': 'Stratpoint'}
        },
        {
            'id': 'skill_1',
            'content': 'Skill: JavaScript and TypeScript for web development',
            'metadata': {'type': 'skill', 'category': 'Languages & Core'}
        }
    ]

    store.add_documents(documents)

    # Search for PyTorch-related content
    results = store.similarity_search("What is CHULOOPA?", k=2)

    assert len(results) > 0
    assert len(results) <= 2
    assert 'content' in results[0]
    assert 'metadata' in results[0]
    assert 'distance' in results[0]

    # Check that CHULOOPA appears in results
    combined_content = ' '.join([r['content'] for r in results])
    assert 'CHULOOPA' in combined_content

def test_vector_store_empty_search(temp_chroma_dir):
    """Test search on empty vector store"""
    store = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_chroma_dir
    )

    results = store.similarity_search("What is CHULOOPA?", k=5)

    assert results == []

def test_vector_store_persistence(temp_chroma_dir):
    """Test that vector store persists data"""
    # Add documents in first instance
    store1 = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_chroma_dir
    )

    documents = [
        {
            'id': 'test_1',
            'content': 'Test document for persistence',
            'metadata': {'type': 'test'}
        }
    ]

    store1.add_documents(documents)
    assert store1.get_collection_count() == 1

    # Create new instance and verify data persists
    store2 = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_chroma_dir
    )

    assert store2.get_collection_count() == 1

    results = store2.similarity_search("persistence", k=1)
    assert len(results) > 0
    assert 'persistence' in results[0]['content']
