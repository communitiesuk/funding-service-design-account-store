"""Flask Local Development Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class UnitTestConfig(Config):

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI + "_UNIT_TEST"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
