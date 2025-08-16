from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(response)
    print(response.json())
    print(response.status_code)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
