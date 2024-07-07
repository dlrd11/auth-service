import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
from models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new test database
Base.metadata.create_all(bind=engine)


# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def test_client():
    # Ensure a clean test database before running tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield client
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)


def test_register_user(test_client):
    response = test_client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert "access_token" in response.json()


def test_register_duplicate_user(test_client):
    response = test_client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_login_user(test_client):
    response = test_client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(test_client):
    response = test_client.post("/auth/login", data={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}


def test_verify_token(test_client):
    response = test_client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    verify_response = test_client.get("/auth/verify", headers=headers)
    assert verify_response.status_code == 200
    assert verify_response.json() == {"username": "testuser"}
