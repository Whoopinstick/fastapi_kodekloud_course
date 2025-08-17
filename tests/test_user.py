from fastapi.testclient import TestClient
from main import app, lifespan
from app.schemas import UserResponse
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = f"postgresql+psycopg://{settings.test_database_user}:{settings.test_database_password}@{settings.test_database_host}:{settings.test_database_port}/{settings.test_database_name}"
engine = create_engine(DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# get this instance instead of the base info
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

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
