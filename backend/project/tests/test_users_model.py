# services/users/project/tests/test_user_model.py

import pytest
from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.utils import add_user


def test_add_user():
    """Đảm bảo có thể thêm user mới với các thuộc tính đúng."""

    user = add_user("justatest", "test@test.com", "test")
    assert user.id is not None
    assert user.username == "justatest"
    assert user.email == "test@test.com"
    assert user.password is not None
    assert user.active is True
    assert user.admin is False


def test_add_user_duplicate_username():
    """Đảm bảo lỗi IntegrityError được raise nếu username trùng lặp."""
    add_user("justatest", "test@test.com", "greaterthaneight")
    duplicate_user = User(
        username="justatest", email="test@test2.com", password="greaterthaneight"
    )
    db.session.add(duplicate_user)
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_add_user_duplicate_email():
    """Đảm bảo lỗi IntegrityError được raise nếu email trùng lặp."""
    add_user("justatest", "test@test.com", "greaterthaneight")
    duplicate_user = User(
        username="justatest2", email="test@test.com", password="greaterthaneight"
    )
    db.session.add(duplicate_user)
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_to_json():
    """Đảm bảo phương thức to_json trả về dict."""
    user = add_user("justatest", "test@test.com", "greaterthaneight")
    assert isinstance(user.to_json(), dict)


def test_passwords_are_random():
    """Đảm bảo password của các user khác nhau là random."""
    user_one = add_user("justatest", "test@test.com", "greaterthaneight")
    user_two = add_user("justatest2", "test@test2.com", "greaterthaneight")
    assert user_one.password != user_two.password


def test_encode_auth_token():
    """Đảm bảo encode_auth_token trả về bytes."""
    user = add_user("justatest", "test@test.com", "test")
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)


def test_decode_auth_token():
    """Đảm bảo decode_auth_token trả về user id đúng."""
    user = add_user("justatest", "test@test.com", "test")
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
    assert User.decode_auth_token(auth_token) == user.id
