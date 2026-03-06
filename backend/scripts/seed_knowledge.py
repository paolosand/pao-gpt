"""Seed knowledge base from markdown files"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.vector_store import VectorStore
from app.config import settings

def chunk_markdown(content: str, filename: str) -> list:
    """
    Chunk markdown content into reasonable-sized pieces

    Split by headers (##) or by paragraphs if no headers
    """
    chunks = []

    # Split by ## headers
    sections = content.split('\n## ')

    for i, section in enumerate(sections):
        if i == 0:
            # First section might not have ## at the start (could be #)
            if section.startswith('# '):
                section = section[2:]  # Remove the #
        else:
            section = '## ' + section  # Add back the ##

        section = section.strip()
        if not section:
            continue

        # If section is very long, split by paragraphs
        if len(section) > 1500:
            paragraphs = section.split('\n\n')
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) < 1500:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para + "\n\n"
            if current_chunk:
                chunks.append(current_chunk.strip())
        else:
            chunks.append(section)

    return chunks

def seed_knowledge_base():
    """Seed knowledge base from markdown files"""
    print("Seeding knowledge base from markdown files...")

    # Get knowledge base directory
    kb_dir = Path(__file__).parent.parent / "data" / "knowledge_base"

    # Initialize vector store
    vector_store = VectorStore()

    documents = []

    # Read all markdown files
    md_files = list(kb_dir.glob("*.md"))

    if not md_files:
        print("No markdown files found in knowledge_base directory")
        return

    for md_file in md_files:
        print(f"Processing {md_file.name}...")

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chunk the content
        chunks = chunk_markdown(content, md_file.stem)

        # Create documents for each chunk
        for i, chunk in enumerate(chunks):
            doc_id = f"{md_file.stem}_{i}"
            documents.append({
                'id': doc_id,
                'content': chunk,
                'metadata': {
                    'source': f'knowledge_base/{md_file.name}',
                    'type': md_file.stem,
                    'chunk_index': i
                }
            })

    # Add documents to vector store
    if documents:
        print(f"\nAdding {len(documents)} chunks to vector store...")
        vector_store.add_documents(documents)

        print(f"✓ Knowledge base seeded successfully!")
        print(f"  Total documents in collection: {vector_store.get_collection_count()}")
        print(f"  ChromaDB location: {settings.chroma_persist_directory}")
    else:
        print("No documents to add")

if __name__ == "__main__":
    seed_knowledge_base()
