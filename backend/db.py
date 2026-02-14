from sqlmodel import create_engine, Session, SQLModel
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# IMPORTANT: Using SYNC engine (NOT async)
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

def init_db():
    """Create all database tables"""
    try:
        SQLModel.metadata.create_all(engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        raise

def get_session():
    """FastAPI dependency for database session"""
    with Session(engine) as session:
        yield session  
def get_sync_session():  
    with Session(engine) as session:  
        yield session  
