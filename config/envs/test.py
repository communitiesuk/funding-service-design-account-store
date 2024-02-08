"""Flask Test Environment Configuration."""

from os import environ

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class TestConfig(Config):
    SECRET_KEY = environ.get("SECRET_KEY", "test")

    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
