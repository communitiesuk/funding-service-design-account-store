"""Flask Local Development Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class DevelopmentConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
