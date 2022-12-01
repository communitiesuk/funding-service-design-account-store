"""
Contains test configuration.
"""
import pytest
from app import create_app
from config import Config
from db import db
from flask_migrate import upgrade
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database


def prep_db(reuse_db=False):
    """Provide the transactional fixtures with access to the database via a
    Flask-SQLAlchemy database connection."""
    no_db = not database_exists(Config.SQLALCHEMY_DATABASE_URI)
    refresh_db = not reuse_db

    if no_db:

        create_database(Config.SQLALCHEMY_DATABASE_URI)

    elif refresh_db:

        drop_database(Config.SQLALCHEMY_DATABASE_URI)
        create_database(Config.SQLALCHEMY_DATABASE_URI)

    upgrade()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        prep_db()
    return app


@pytest.fixture(scope="function")
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().app_context() as app_context:
        with app_context.app.test_client() as test_client:
            yield test_client


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access
    to the database via a Flask-SQLAlchemy
    database connection.
    """
    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):
    pass
