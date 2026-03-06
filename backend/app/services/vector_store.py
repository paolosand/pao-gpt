"""ChromaDB vector store interface"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict
from app.config import settings

class VectorStore:
    """ChromaDB vector store wrapper"""

    def __init__(self, collection_name: str = None, persist_directory: str = None):
        """Initialize vector store with ChromaDB"""
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        self.collection_name = collection_name or settings.chroma_collection_name

        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[dict]):
        """
        Add documents to vector store

        Args:
            documents: List of dicts with 'content', 'metadata', 'id' keys
        """
        doc_texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        ids = [doc['id'] for doc in documents]

        self.collection.add(
            documents=doc_texts,
            metadatas=metadatas,
            ids=ids
        )

    def similarity_search(self, query: str, k: int = 5) -> List[dict]:
        """
        Search for similar documents

        Args:
            query: Query string
            k: Number of results to return

        Returns: List of {content, metadata, distance} dicts
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        documents = []
        for i, doc in enumerate(results["documents"][0]):
            documents.append({
                "content": doc,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0.0
            })

        return documents

    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()

# Global instance
_vector_store = None

def get_vector_store() -> VectorStore:
    """Get or create vector store singleton"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
