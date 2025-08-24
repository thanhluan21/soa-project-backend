# services/users/project/tests/base.py

import pytest
from project import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
