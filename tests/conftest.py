# special file for pytest.
# fixtures and hooks defined in this file are accessible in all tests in the directory and subdirectories

import pytest
from fastapi.testclient import TestClient
from main import app
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = f"postgresql+psycopg://{settings.test_database_user}:{settings.test_database_password}@{settings.test_database_host}:{settings.test_database_port}/{settings.test_database_name}"
engine = create_engine(DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# you could change fixture scope so the database isn't destroyed after each test/function
# maybe not a best practice
# default scope is function
@pytest.fixture(scope="function")
def session():
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# create user fixture to be passed into other tests
@pytest.fixture()
def test_user(client):
    user_data = {"email": "hello@gmail.com", "password": "Password!23"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user
