"""
This file is the entry point for flask run.
"""
import connexion
from flask import Flask


def create_app() -> Flask:
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/")

    flask_app = connexion_app.app

    connexion_app.add_api("api.yml")

    return flask_app


app = create_app()
