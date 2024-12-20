"""Flask configuration."""

import logging
from os import environ
from pathlib import Path

from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class DefaultConfig(object):
    #  Application Config
    FLASK_ENV = CommonConfig.FLASK_ENV
    SECRET_KEY = CommonConfig.SECRET_KEY
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
