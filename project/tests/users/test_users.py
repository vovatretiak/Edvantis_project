from fastapi.testclient import TestClient

from main import app
from project.utils import create_access_token
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
    response = client.get("/users/", params={"offset": 1, "limit": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "jane123"


def test_registration():
    """tests post method to create new user"""
    data = {
        "username": "testuser",
        "email": "test@mail.com",
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

    response = client.get("/users/")
    assert response.status_code == 200
    get_data = response.json()
    assert len(get_data) == 3

    # invalid username
    data["username"] = "testuser!"
    response = client.post("/users/registration", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "must be alphanumeric"
    # passwords do not match
    data["username"] = "testuser"
    data["confirm_password"] = "1"
    response = client.post("/users/registration", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "passwords do not match"


def test_login():
    """tests post method to create token for user"""
    data = {"username": "john123", "password": "password"}
    response = client.post("/users/login", data=data)
    assert response.status_code == 201
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
    # wrong password
    data = {"username": "john123", "password": "password_wrong"}
    response = client.post("/users/login", data=data)
    assert response.status_code == 403


def test_read_me():
    """tests get method to show current user"""
    user_access_token = create_access_token("john123")
    response = client.get(
        "/users/profile", headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "john123"
    assert "id" in data
    assert "reviews" in data
    # wrong token
    user_access_token = create_access_token("john123_wrong")
    response = client.get(
        "/users/profile", headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 401


def test_update_me():
    """tests put method to update current user"""
    data = {
        "username": "updated_jonh",
        "email": "updated_jonh@mail.com",
        "password": "newpass",
        "confirm_password": "newpass",
    }
    user_access_token = create_access_token("john123")
    response = client.put(
        "/users/profile",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=data,
    )
    # invalid username
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "must be alphanumeric"
    # passwords do not match
    data["username"] = "updatedjonh"
    data["confirm_password"] = "1"
    response = client.put(
        "/users/profile",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=data,
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "passwords do not match"
    # correct values
    data["confirm_password"] = "newpass"
    response = client.put(
        "/users/profile",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=data,
    )
    assert response.status_code == 202
    response_data = response.json()
    assert "id" in response_data
    assert response_data["username"] == "updatedjonh"
    assert response_data["email"] == "updated_jonh@mail.com"
    assert verify_password(data["password"], response_data["password"])


def test_delete_me():
    """tests delete method to delete current user"""
    user_access_token = create_access_token("john123")

    response = client.delete(
        "/users/profile", headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 204
