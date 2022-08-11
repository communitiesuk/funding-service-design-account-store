"""
Constructs the flask app using the typical create_app function.
"""
import connexion
from config import Config
from flask import Blueprint, Flask, current_app
from fsd_utils.logging import logging
from flask import request

from healthcheck import Healthcheck
from db import db, migrate


def create_app() -> Flask:
    connexion_options = {"swagger_url": "/"}
    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir=Config.FLASK_ROOT + "/openapi/",
        options=connexion_options,
    )
    connexion_app.add_api(Config.FLASK_ROOT + "/openapi/api.yml")

    # Configure Flask App
    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")

    # Initialise logging
    logging.init_app(flask_app)


    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)
    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(
        flask_app, db, directory="db/migrations", render_as_batch=True
    )

    # Add healthchecks to flask_app
    health = Healthcheck(flask_app)
    health.add_check(check_running)
    health.add_check(check_db)

    return flask_app

def check_running():
    return "OK"

def check_db():
    db.session.execute("SELECT 1")
    return "OK"

app = create_app()
