from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config.Config import Config

engine = create_engine(Config().DATABASE_URL)

# Base para os modelos
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    with SessionLocal() as session:
        yield session
