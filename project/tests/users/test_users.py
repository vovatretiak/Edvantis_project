from fastapi.testclient import TestClient

from main import app
from project.utils import create_access_token
from project.utils import verify_password


client = TestClient(app)


def test_all_users():
    """tests get method to get all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    assert users[0]["username"] == "john123"
    assert users[1]["username"] == "jane123"
    assert verify_password("password", users[0]["password"])
    assert verify_password("password2", users[1]["password"])
    assert users[0]["rank"] == "9 kyu"
    assert users[1]["rank"] == "9 kyu"
    # with params
    response = client.get("/users/", params={"offset": 1, "limit": 1})
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["username"] == "jane123"


def test_registration():
    """tests post method to create new user"""
    payload = {
        "username": "testuser",
        "email": "test@mail.com",
        "password": "1234567890",
        "confirm_password": "1234567890",
    }
    response = client.post("/users/registration", json=payload)
    assert response.status_code == 201
    new_user = response.json()
    assert "id" in new_user
    assert verify_password(payload["password"], new_user["password"])
    assert new_user["rank"] == "9 kyu"
    assert "reviews" in new_user

    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 3

    # invalid username
    payload["username"] = "testuser!"
    response = client.post("/users/registration", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "must be alphanumeric"
    # passwords do not match
    payload["username"] = "testuser"
    payload["confirm_password"] = "1"
    response = client.post("/users/registration", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "passwords do not match"


def test_login():
    """tests post method to create token for user"""
    payload = {"username": "john123", "password": "password"}
    response = client.post("/users/login", data=payload)
    assert response.status_code == 201
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    # wrong password
    payload = {"username": "john123", "password": "password_wrong"}
    response = client.post("/users/login", data=payload)
    assert response.status_code == 403


def test_read_me():
    """tests get method to show current user"""
    user_access_token = create_access_token("john123")
    response = client.get(
        "/users/profile", headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == "john123"
    assert "id" in user
    assert "reviews" in user
    # wrong token
    user_access_token = create_access_token("john123_wrong")
    response = client.get(
        "/users/profile", headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 401


def test_update_me():
    """tests put method to update current user"""
    payload = {
        "username": "updated_jonh",
        "email": "updated_jonh@mail.com",
        "password": "newpass",
        "confirm_password": "newpass",
    }
    user_access_token = create_access_token("john123")
    response = client.put(
        "/users/profile",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=payload,
    )
    # invalid username
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "must be alphanumeric"
    # passwords do not match
    payload["username"] = "updatedjonh"
    payload["confirm_password"] = "1"
    response = client.put(
        "/users/profile",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=payload,
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "passwords do not match"
    # correct values
    payload["confirm_password"] = "newpass"
    response = client.put(
        "/users/profile",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=payload,
    )
    assert response.status_code == 202
    updated_user = response.json()
    assert "id" in updated_user
    assert updated_user["username"] == "updatedjonh"
    assert updated_user["email"] == "updated_jonh@mail.com"
    assert verify_password(payload["password"], updated_user["password"])


def test_delete_me():
    """tests delete method to delete current user"""
    user_access_token = create_access_token("john123")

    response = client.delete(
        "/users/profile", headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 204
