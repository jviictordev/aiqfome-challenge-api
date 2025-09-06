from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.Config import Config

Base = declarative_base()
engine = create_engine(Config().DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    with SessionLocal() as session:
        yield session
