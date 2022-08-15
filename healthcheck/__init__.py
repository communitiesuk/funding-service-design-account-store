from json import dumps
from flask import current_app

class Healthcheck(object):

    def __init__(self, app):
        self.flask_app = app
        self.flask_app.add_url_rule("/healthcheck", view_func=self.healthcheck_view)
        self.checks = []

    def healthcheck_view(self):
        responseCode = 200
        response = {"checks":[]}
        for func in self.checks:
            try:
                result = func()
                current_app.logger.debug(f"Check {func.__name__} returned {result}")
                response["checks"].append({func.__name__ : result[1]})
                if result[0] == False:
                    responseCode = 500
            except Exception as e:
                response["checks"].append({func.__name__ : "Failed - check logs"})
                current_app.logger.exception(f"Check {func.__name__} failed with an exception")
                responseCode = 500
        return response, responseCode

    def add_check(self, check_func):
        self.checks.append(check_func)

    