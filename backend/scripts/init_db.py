"""Initialize PostgreSQL database with schema"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.models import Base
from app.database.session import engine
from app.config import settings

def init_database():
    """Create all tables"""
    print(f"Initializing database: {settings.database_url}")

    # Create tables
    Base.metadata.create_all(bind=engine)

    print("✓ Database tables created successfully")
    print("  - conversations")
    print("  - knowledge_updates")
    print("  - query_patterns")

if __name__ == "__main__":
    init_database()
