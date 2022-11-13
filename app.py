"""
Constructs the flask app using the typical create_app function.
"""
import connexion
from config import Config
from db import db
from db import migrate
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from core.account import update_account_roles


def create_app() -> Flask:
    init_sentry()
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
    health.add_check(FlaskRunningChecker())
    health.add_check(DbChecker(db))

    return flask_app


app = create_app()


@app.cli.command("update-account-roles")
def update_account_roles_cli():
    roles, status = update_account_roles()
    for email, role in roles.items():
        print("--------------\nROLES UPDATED\n--------------")
        print(email[0:4] + "****" + email[-6:] + " - " + role)
