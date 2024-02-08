"""Flask Production Environment Configuration."""

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class ProductionConfig(Config):
    pass
