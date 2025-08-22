import pytest
import jwt
from jwt.exceptions import InvalidTokenError
from tests.database import session, client
from app.schemas import UserResponse, Token
from app.config import settings

# create user fixture to be passed into other tests
@pytest.fixture()
def test_user(client):
    user_data = {"email": "hello@gmail.com", "password": "Password!23"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user



def test_create_user(client):
    # this will actually create an entry in the database
    response = client.post("/users", json={"email": "hello123@gmail.com", "password": "Password!23"})
    response_data = response.json()
    print(response_data)
    new_user = UserResponse(id=response_data["id"], email=response_data["email"], created_at=response_data["created_at"])
    print("info from test_create_user")
    print(new_user)
    print(new_user.email)
    assert new_user.email == "hello123@gmail.com"
    assert response.status_code == 201

# update test to use test_user fixture, so it's not dependent on test_create_user function
def test_login_user(client, test_user):
    response = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    response_data = response.json()
    print("info from test_login_user")
    print(response_data)

    # get the token
    response_token = Token(access_token=response_data["access_token"], token_type=response_data["token_type"])
    print(f"response_token: {response_token}")

    # validate the token
    payload = jwt.decode(response_token.access_token , settings.secret_key, algorithms=[settings.algorithm])
    print(f"payload: {payload}")
    user_id_from_token = payload.get("user_id")

    assert user_id_from_token == test_user["id"]
    assert response_token.token_type == "bearer"
    assert response.status_code == 200
