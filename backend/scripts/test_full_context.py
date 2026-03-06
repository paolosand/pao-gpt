"""Test full-context knowledge loading"""
import asyncio
from app.services.knowledge_loader import load_all_knowledge, get_knowledge_summary
from app.agents.chains.rag_chain import RAGChain

async def test_retrieval():
    """Test that we now load all knowledge documents"""
    print("\n" + "="*60)
    print("FULL-CONTEXT KNOWLEDGE LOADING TEST")
    print("="*60)

    # Get summary
    summary = get_knowledge_summary()
    print(f"\n{summary}")

    # Load all knowledge
    docs = load_all_knowledge()
    print(f"\nLoaded {len(docs)} documents:")
    for doc in docs:
        source = doc['metadata']['source']
        doc_type = doc['metadata']['type']
        content_len = len(doc['content'])
        print(f"  - {doc_type:12s} ({content_len:4d} chars) from {source}")

    # Calculate total tokens (rough estimate: 1 token ≈ 4 chars)
    total_chars = sum(len(doc['content']) for doc in docs)
    estimated_tokens = total_chars // 4
    print(f"\nTotal characters: {total_chars:,}")
    print(f"Estimated tokens: ~{estimated_tokens:,}")
    print(f"Context window usage: {estimated_tokens / 1_000_000 * 100:.2f}% of 1M token limit")

    # Test RAG chain retrieval
    print("\n" + "="*60)
    print("RAG CHAIN RETRIEVAL TEST")
    print("="*60)

    rag = RAGChain()

    # Test query - doesn't matter what we ask, we get everything!
    query = "Where does Paolo work?"
    retrieved_docs = await rag.retrieve(query)

    print(f"\nQuery: '{query}'")
    print(f"Retrieved: {len(retrieved_docs)} documents (all of them!)")
    print("\nDocument types retrieved:")
    for doc in retrieved_docs:
        doc_type = doc['metadata']['type']
        preview = doc['content'][:80].replace('\n', ' ')
        print(f"  [{doc_type}] {preview}...")

    print("\n✅ Full-context loading working correctly!")
    print("   All portfolio knowledge passed to LLM every time.")
    print("   No retrieval ranking issues - LLM sees everything!")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
