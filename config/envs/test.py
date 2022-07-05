"""Flask Test Environment Configuration."""
from os import environ

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class TestConfig(Config):

    SECRET_KEY = environ.get("SECRET_KEY", "test")
