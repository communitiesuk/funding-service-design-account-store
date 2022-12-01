"""Flask Local Development Environment Configuration."""
import logging

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class DevelopmentConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
