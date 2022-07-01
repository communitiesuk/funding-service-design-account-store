"""Flask Production Environment Configuration."""
from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


# TODO : Uncomment the following if using a GovPaaS VcapServices
#  redis instance for session management.
#  The VcapServices helper class has methods to parse the chosen
#  redis instance url from the Cloud Foundry VcapServices env dictionary
# import redis
# import json
# from os import environ
# from dataclasses import dataclass
#
#
# @dataclass
# class VcapServices(object):
#
#     services: dict
#
#     @staticmethod
#     def from_env_json(json_string: str):
#         json_dict = dict(json.loads(json_string))
#         vcap_services = VcapServices(services=json_dict)
#         return vcap_services
#
#     def get_service_by_name(self, group_key: str, name: str) -> dict:
#         service_group = self.services.get(group_key)
#         if service_group:
#             for service in service_group:
#                 if service.get("name") == name:
#                     return service
#             raise Exception(f"Service name '{name}' not found")
#         raise Exception(f"Service group '{group_key}' not found")
#
#     def get_service_credentials_value(
#         self, group_key: str, name: str, key: str
#     ):
#         service = self.get_service_by_name(group_key, name)
#         return service.get("credentials").get(key)


@configclass
class ProductionConfig(Config):

    # TODO: Uncomment the following if using a GovPaaS VcapServices
    #  redis instance for session management
    # # GOV.UK PaaS
    # VCAP_SERVICES = VcapServices.from_env_json(environ.get("VCAP_SERVICES"))
    #
    # # Redis
    # REDIS_INSTANCE_NAME = "funding-service-TEMPLATE-production"
    # REDIS_INSTANCE_URI = VCAP_SERVICES.get_service_credentials_value(
    #     "redis", REDIS_INSTANCE_NAME, "uri"
    # )
    # REDIS_SESSIONS_URL = REDIS_INSTANCE_URI + "/0"
    # SESSION_REDIS = redis.from_url(REDIS_SESSIONS_URL)
    pass
