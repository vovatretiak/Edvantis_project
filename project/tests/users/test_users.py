from fastapi.testclient import TestClient

from main import app
from project.utils import verify_password


client = TestClient(app)


def test_all_users():
    """tests get method to get all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "john123"
    assert data[1]["username"] == "jane123"
    assert verify_password("password", data[0]["password"])
    assert verify_password("password2", data[1]["password"])
    assert data[0]["rank"] == "9 kyu"
    assert data[1]["rank"] == "9 kyu"


def test_registration():
    """tests post method to create new user"""
    data = {
        "username": "testuser",
        "email": "test@email.com",
        "password": "1234567890",
        "confirm_password": "1234567890",
    }
    response = client.post("/users/registration", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert verify_password(data["password"], response_data["password"])
    assert response_data["rank"] == "9 kyu"
    assert "reviews" in response_data


def test_login():
    """tests post method to create token for user"""
    data = {"username": "john123", "password": "password"}
    response = client.post("/users/login", data=data)
    assert response.status_code == 201
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
