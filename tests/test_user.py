from fastapi.testclient import TestClient
from main import app
from app.schemas import UserResponse

client = TestClient(app)

def test_create_user():
    # this will actually create an entry in the database
    response = client.post("/users", json={"email": "hello123@gmail.com", "password": "Password!23"})
    response_data = response.json()
    print(response_data)
    new_user = UserResponse(id=response_data["id"], email=response_data["email"], created_at=response_data["created_at"])
    print(new_user)
    print(new_user.email)
    assert new_user.email == "hello123@gmail.com"
    assert response.status_code == 201
