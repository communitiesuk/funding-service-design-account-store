"""Flask Dev Pipeline Environment Configuration."""
import logging

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class DevConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
