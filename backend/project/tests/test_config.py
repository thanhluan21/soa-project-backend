from project import create_app


def test_config_dev(app):
    app.config.from_object("project.config.DevelopmentConfig")
    assert app.config["TESTING"] == True
    assert (
        app.config["SQLALCHEMY_DATABASE_URI"]
        == "postgresql://postgres:postgres@db:5432/users_dev"
    )
    # Thêm test khác như check secret key hoặc debug mode nếu có


def test_config_prd(app):
    app.config.from_object("project.config.ProductionConfig")
    assert app.config["TESTING"] == True
    assert (
        app.config["SQLALCHEMY_DATABASE_URI"]
        == "postgresql://postgres:postgres@db:5432/users_dev"
    )
    # Thêm test khác như check secret key hoặc debug mode nếu có
