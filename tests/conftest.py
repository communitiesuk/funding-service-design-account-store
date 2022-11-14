"""
Contains test configuration.
"""
import os

import flask_migrate
import pytest
from config import Config
from app import create_app


class SqliteTestDB:
    @classmethod
    def remove(cls):
        flask_root = Config.FLASK_ROOT
        db_file_name = Config.SQLITE_DB_NAME
        db_file_path = os.path.join(flask_root, db_file_name)
        if os.path.exists(db_file_path):
            os.remove(db_file_path)

    @classmethod
    def create(cls):
        cls.remove()
        flask_migrate.upgrade()


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture(scope="function")
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().app_context() as app_context:
        SqliteTestDB.create()
        with app_context.app.test_client() as test_client:
            yield test_client
        SqliteTestDB.remove()
