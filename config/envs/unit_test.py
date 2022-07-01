"""Flask Local Development Environment Configuration."""
import logging
from os import path

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    SQLITE_DB_NAME = "test_sqlite.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
        Config.FLASK_ROOT, SQLITE_DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
