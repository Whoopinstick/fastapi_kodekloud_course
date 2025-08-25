# special file for pytest.
# fixtures and hooks defined in this file are accessible in all tests in the directory and subdirectories

import pytest
from fastapi.testclient import TestClient
from main import app
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app.models import Post

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


# create a fixture to create a fake token to be used in various tests
@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


# a fixture to give us an authenticated user
@pytest.fixture()
def authorized_client(client, token):
    # add bearer token to the client
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# create sample posts
@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    },
        {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
            "title": "3rd title",
            "content": "3rd content",
            "user_id": test_user['id']
    }]

    # map post data to Post
    # def create_post_model(post):
    #     return Post(**post)

    # post_map_list = list(map(create_post_model, posts_data))
    # use lambda instead, no need for 1 liner create_post_model function
    post_map_list = map(lambda x: Post(**x), posts_data)

    session.add_all(post_map_list)
    session.commit()
    session.query(Post).all()

    return post_map_list