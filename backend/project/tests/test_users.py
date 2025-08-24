# services/users/project/tests/test_users.py

import json
import pytest

from project import db
from project.api.models import User
from project.tests.utils import add_user


def test_users(client):
    """Đảm bảo route /ping hoạt động đúng."""
    response = client.get("/users/ping")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert "pong!" in data["message"]
    assert "success" in data["status"]


def test_add_user(client):
    """Đảm bảo có thể thêm user mới vào database."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.admin = True
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "michael",
                "email": "michael@mherman.org",
                "password": "greaterthaneight",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert "michael@mherman.org was added!" in data["message"]
    assert "success" in data["status"]


def test_add_user_invalid_json(client):
    """Đảm bảo lỗi được trả về nếu JSON object rỗng."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.admin = True
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_invalid_json_keys(client):
    """Đảm bảo lỗi được trả về nếu JSON object thiếu key username."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.admin = True
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.post(
        "/users",
        data=json.dumps(
            {"email": "michael@mherman.org", "password": "greaterthaneight"}
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_invalid_json_keys_no_password(client):
    """Đảm bảo lỗi được trả về nếu JSON object thiếu key password."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.admin = True
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@reallynotreal.com"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_duplicate_email(client):
    """Đảm bảo lỗi được trả về nếu email đã tồn tại."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    user = User.query.filter_by(email="test@test.com").first()
    user.admin = True
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    client.post(
        "/users",
        data=json.dumps(
            {
                "username": "michael",
                "email": "michael@mherman.org",
                "password": "greaterthaneight",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@mherman.org"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Sorry. That email already exists." in data["message"]
    assert "fail" in data["status"]


def test_single_user(client):
    """Đảm bảo lấy thông tin single user hoạt động đúng."""
    with client.application.app_context():
        user = add_user("michael", "michael@mherman.org", "greaterthaneight")
    response = client.get(f"/users/{user.id}")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert "michael" in data["data"]["username"]
    assert "michael@mherman.org" in data["data"]["email"]
    assert "success" in data["status"]


def test_single_user_no_id(client):
    """Đảm bảo lỗi được trả về nếu không cung cấp id."""
    response = client.get("/users/blah")
    data = json.loads(response.data.decode())
    assert response.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]


def test_single_user_incorrect_id(client):
    """Đảm bảo lỗi được trả về nếu id không tồn tại."""
    response = client.get("/users/999")
    data = json.loads(response.data.decode())
    assert response.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]


def test_all_users(client):
    """Đảm bảo lấy tất cả users hoạt động đúng."""
    with client.application.app_context():
        add_user("michael", "michael@mherman.org", "test")
        add_user("fletcher", "fletcher@noteal.com", "test")
    response = client.get("/users")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data["data"]["users"]) == 2
    assert "michael" in data["data"]["users"][0]["username"]
    assert "michael@mherman.org" in data["data"]["users"][0]["email"]
    assert data["data"]["users"][0]["active"] is True
    assert data["data"]["users"][0]["admin"] is False
    assert "fletcher" in data["data"]["users"][1]["username"]
    assert "fletcher@noteal.com" in data["data"]["users"][1]["email"]
    assert data["data"]["users"][1]["active"] is True
    assert data["data"]["users"][1]["admin"] is False
    assert "success" in data["status"]


def test_main_no_users(client):
    """Đảm bảo route chính hoạt động đúng khi không có users."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>All Users</h1>" in response.data
    assert b"<p>No users!</p>" in response.data


def test_main_with_users(client):
    """Đảm bảo route chính hoạt động đúng khi có users."""
    with client.application.app_context():
        add_user("michael", "michael@mherman.org", "greaterthaneight")
        add_user("fletcher", "fletcher@notreal.com", "greaterthaneight")
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>All Users</h1>" in response.data
    assert b"<p>No users!</p>" not in response.data
    assert b"michael" in response.data
    assert b"fletcher" in response.data


def test_main_add_user(client):
    """Đảm bảo có thể thêm user mới qua route chính."""
    response = client.post(
        "/",
        data=dict(username="michael", email="michael@sonotreal.com", password="test"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"<h1>All Users</h1>" in response.data
    assert b"<p>No users!</p>" not in response.data
    assert b"michael" in response.data


def test_add_user_inactive(client):
    """Đảm bảo lỗi khi thêm user với tài khoản inactive."""
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
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "michael",
                "email": "michael@sonotreal.com",
                "password": "test",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "Provide a valid auth token."
    assert response.status_code == 401


def test_add_user_not_admin(client):
    """Đảm bảo lỗi khi thêm user mà không phải admin."""
    with client.application.app_context():
        add_user("test", "test@test.com", "test")
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "michael",
                "email": "michael@sonotreal.com",
                "password": "test",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = json.loads(response.data.decode())
    assert data["status"] == "fail"
    assert data["message"] == "You do not have permission to do that."
    assert response.status_code == 401
