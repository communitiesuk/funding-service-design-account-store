"""Flask Local Development Environment Configuration."""
import logging
from os import environ
from os import path

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"
    ADMIN_SECRET = "a-secret-key"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    SQLITE_DB_NAME = "test_sqlite.db"
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + path.join(Config.FLASK_ROOT, "sqlite.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
