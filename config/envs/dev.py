"""Flask Dev Pipeline Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class DevConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
    SQLALCHEMY_TRACK_MODIFICATIONS = False
