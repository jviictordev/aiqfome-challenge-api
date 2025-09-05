from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config.Config import Config

engine = create_engine(Config().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
