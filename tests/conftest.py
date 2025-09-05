import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config.Database import get_session
from main import app
from models.Models import table_registry


@pytest.fixture
def client():
    def get_session_override():
        return session
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('postgresql://postgres:xtleqx74@localhost:5432/aiqfome-database-test')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
