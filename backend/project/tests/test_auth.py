# services/users/project/tests/test_auth.py

import json
from flask import current_app

from project import db
from project.api.models import User
from project.tests.utils import add_user


def test_user_registration(client):
    """Đảm bảo việc đăng ký user mới hoạt động đúng."""
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "justatest",
                "email": "test@test.com",
                "password": "123456",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert data["message"] == "Successfully registered."
    assert data["auth_token"]
    assert response.content_type == "application/json"
    assert response.status_code == 201


def test_user_registration_duplicate_email(client):
    """Đảm bảo lỗi được trả về nếu email đã tồn tại khi đăng ký."""

    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "michael", "email": "test@test.com", "password": "test"}
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Sorry. That user already exists." in data["message"]
    assert "fail" in data["status"]


def test_user_registration_duplicate_username(client):
    """Đảm bảo lỗi được trả về nếu username đã tồn tại khi đăng ký."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "test", "email": "test@test.com2", "password": "test"}
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Sorry. That user already exists." in data["message"]
    assert "fail" in data["status"]


def test_user_registration_invalid_json(client):
    """Đảm bảo lỗi được trả về nếu JSON object rỗng khi đăng ký."""
    response = client.post(
        "/auth/register", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_user_registration_invalid_json_keys_no_username(client):
    """Đảm bảo lỗi được trả về nếu thiếu key username trong JSON khi đăng ký."""
    response = client.post(
        "/auth/register",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_user_registration_invalid_json_keys_no_email(client):
    """Đảm bảo lỗi được trả về nếu thiếu key email trong JSON khi đăng ký."""
    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "justatest", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_user_registration_invalid_json_keys_no_password(client):
    """Đảm bảo lỗi được trả về nếu thiếu key password trong JSON khi đăng ký."""
    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "justatest", "email": "test@test.com"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_registered_user_login(client):
    """Đảm bảo user đã đăng ký có thể login thành công."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert data["message"] == "Successfully logged in."
    assert data["auth_token"]
    assert response.content_type == "application/json"
    assert response.status_code == 200


def test_not_registered_user_login(client):
    """Đảm bảo lỗi được trả về nếu user chưa đăng ký cố login."""
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "User does not exist."
    assert response.content_type == "application/json"
    assert response.status_code == 404


def test_valid_logout(client):
    """Đảm bảo logout với token hợp lệ hoạt động đúng."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.get("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert data["message"] == "Successfully logged out."
    assert response.status_code == 200


def test_invalid_logout_expired_token(client):
    """Đảm bảo lỗi được trả về khi logout với token hết hạn."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.get("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "Signature expired. Please log in again."
    assert response.status_code == 401


def test_invalid_logout(client):
    """Đảm bảo lỗi được trả về khi logout với token không hợp lệ."""
    response = client.get("/auth/logout", headers={"Authorization": "Bearer invalid"})
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "Invalid token. Please log in again."
    assert response.status_code == 401


def test_user_status(client):
    """Đảm bảo lấy status user với token hợp lệ hoạt động đúng."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.get("/auth/status", headers={"Authorization": f"Bearer {token}"})
    data = json.loads(response.data.decode())
    assert data["status"] == "success"
    assert data["data"] is not None
    assert data["data"]["username"] == "test"
    assert data["data"]["email"] == "test@test.com"
    assert data["data"]["active"]
    assert not data["data"]["admin"]
    assert response.status_code == 200


def test_invalid_status(client):
    """Đảm bảo lỗi được trả về khi lấy status với token không hợp lệ."""
    response = client.get("/auth/status", headers={"Authorization": "Bearer invalid"})
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "Invalid token. Please log in again."
    assert response.status_code == 401


def test_invalid_logout_inactive(client):
    """Đảm bảo lỗi được trả về khi logout với user inactive."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.active = False
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.get("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "Provide a valid auth token."
    assert response.status_code == 401


def test_invalid_status_inactive(client):
    """Đảm bảo lỗi được trả về khi lấy status với user inactive."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.active = False
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.get("/auth/status", headers={"Authorization": f"Bearer {token}"})
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "Provide a valid auth token."
    assert response.status_code == 401
