"""Flask Local Development Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class DevelopmentConfig(Config):
    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
