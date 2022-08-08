from fastapi.testclient import TestClient

from main import app
from project.utils import verify_password


client = TestClient(app)


def test_all_users():
    """test method to get all users"""
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
