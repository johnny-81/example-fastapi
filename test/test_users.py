import jwt
import pytest

from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users",
        json={
            "email": "hello123@gmail.com",
            "password": "password123",
        },
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):

    res = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    new_token = schemas.Token(**res.json())

    payload = jwt.decode(
        new_token.access_token, settings.secret_key, algorithms=["HS256"]
    )
    id: str = payload.get("user_id")

    assert id == test_user["id"]
    assert res.status_code == 200
    assert new_token.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("tiep@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 403),
        ("wrongemail@gmail.com", None, 403),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
