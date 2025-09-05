import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config.Database import Base, get_session  # seu método original de criar session

# Cria um engine para teste (usa SQLite em memória)
DATABASE_URL = 'postgresql://postgres:xtleqx74@localhost:5432/aiqfome-database-test'
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas para os testes
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture para injetar session de teste
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Sobrescreve a dependência do FastAPI
@pytest.fixture(autouse=True)
def override_get_session(db_session):
    def _override():
        yield db_session
    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()

# Cliente de teste do FastAPI
@pytest.fixture
def client():
    return TestClient(app)
