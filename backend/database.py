import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import DATABASE_URL

logger = logging.getLogger("reywebstudio.database")

def get_engine_and_db_url():
    db_url = DATABASE_URL
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        # Test connection
        with engine.connect() as conn:
            pass
        print("[DATABASE] Connected to PostgreSQL successfully.")
        return engine
    except Exception as e:
        print(f"[DATABASE] Could not connect to PostgreSQL ({e}). Falling back to SQLite for local execution.")
        fallback_url = "sqlite:///./reywebstudio.db"
        engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
        return engine

engine = get_engine_and_db_url()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
