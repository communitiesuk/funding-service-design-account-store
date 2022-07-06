"""
Constructs the flask app using the typical create_app function.
"""
import connexion
from flask import Flask
from config import Config

from fsd_utils.logging import logging


def create_app() -> Flask:

    connexion_options = {"swagger_url": "/"}
    connexion_app = connexion.FlaskApp(
        "Account Store",
        specification_dir=Config.FLASK_ROOT + "/openapi/",
        options=connexion_options,
    )
    connexion_app.add_api(Config.FLASK_ROOT + "/openapi/api.yml")

    # Configure Flask App
    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")

    # Initialise logging
    logging.init_app(flask_app)

    return flask_app
