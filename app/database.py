from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings

_url = settings.effective_database_url
_engine_kwargs: dict = {"connect_args": {"check_same_thread": False}}

# In-memory SQLite needs StaticPool so every connection shares the same
# database.  Without it each connect() creates a separate empty DB.
if _url == "sqlite:///:memory:" or ":memory:" in _url:
    _engine_kwargs["poolclass"] = StaticPool

engine = create_engine(_url, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
