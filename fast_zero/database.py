from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fast_zero.settings import settings

# Cria o engine usando PostgreSQL (ou SQLite em dev)
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,    # logs de SQL em dev
    future=True,  # API 2.0 do SQLAlchemy
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

def get_session():
    """Depêndencia FastAPI - retorna uma sessão do DB e fecha ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()