import connexion
from flask import Flask
from utils.definitions import get_project_root

project_root_path = str(get_project_root())


def create_app() -> Flask:

    options = {"swagger_url": "/"}

    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir=project_root_path + "/openapi/",
        options=options,
    )

    flask_app = connexion_app.app

    connexion_app.add_api(project_root_path + "/openapi/api.yml")

    return flask_app
