"""Flask Dev Pipeline Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class DevConfig(DefaultConfig):
    #  Application Config

    # Logging
    FSD_LOG_LEVEL = logging.INFO
    SQLALCHEMY_TRACK_MODIFICATIONS = False
