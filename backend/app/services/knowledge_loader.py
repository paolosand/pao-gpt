"""Load all knowledge base documents for full-context prompting"""
import os
from pathlib import Path
from typing import List, Dict

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent.parent / "data" / "knowledge_base"

def load_all_knowledge() -> List[Dict]:
    """
    Load all markdown files from knowledge base directory.
    Returns list of documents with content and metadata.
    """
    documents = []

    if not KNOWLEDGE_BASE_DIR.exists():
        return documents

    # Load all .md files
    for md_file in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            documents.append({
                'content': content,
                'metadata': {
                    'source': f'knowledge_base/{md_file.name}',
                    'type': md_file.stem,
                }
            })
        except Exception as e:
            print(f"Warning: Failed to load {md_file}: {e}")
            continue

    return documents

def get_knowledge_summary() -> str:
    """Get a summary of available knowledge"""
    docs = load_all_knowledge()
    return f"Loaded {len(docs)} knowledge base documents: {', '.join(d['metadata']['type'] for d in docs)}"
