"""
Constructs the flask app using the typical create_app function.
"""
import connexion
from config import Config
from flask import Blueprint, Flask, current_app
from fsd_utils.logging import logging
from flask import request


def create_app() -> Flask:
    healthcheck = Blueprint('healthcheck', __name__)


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

    from db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)
    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(
        flask_app, db, directory="db/migrations", render_as_batch=True
    )
    @healthcheck.route('/healthcheck')
    def show():
        try:
            if request.args.get("database"):
                db.session.execute('SELECT 1')
            return 'OK', 200
        except:
            current_app.logger.exception("Healthcheck failed on db call")
            return 'Fail', 500

    with flask_app.app_context():
        flask_app.register_blueprint(healthcheck)

    return flask_app


app = create_app()
