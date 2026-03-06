"""Initialize PostgreSQL database with schema"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.models import Base
from app.database.session import engine
from app.config import settings

def init_database():
    """Initialize the database by creating all tables"""
    try:
        # Sanitize URL for logging (hide password)
        db_url = str(settings.database_url)
        if '@' in db_url:
            # Hide password in connection string
            parts = db_url.split('@')
            user_pass = parts[0].split('://')[-1]
            if ':' in user_pass:
                user = user_pass.split(':')[0]
                safe_url = db_url.replace(user_pass, f"{user}:****")
            else:
                safe_url = db_url
        else:
            safe_url = db_url

        print(f"Initializing database: {safe_url}")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        print("  - conversations")
        print("  - knowledge_updates")
        print("  - query_patterns")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise

if __name__ == "__main__":
    init_database()
