from json import dumps
from flask import current_app

class Healthcheck(object):

    def __init__(self, app):
        self.flask_app = app
        self.flask_app.add_url_rule("/healthcheck", view_func=self.healthcheck_view)
        self.checkers = []

    def healthcheck_view(self):
        responseCode = 200
        response = {"checks":[]}
        for checker in self.checkers:
            try:
                result = checker.check()
                current_app.logger.debug(f"Check {checker.name} returned {result}")
                response["checks"].append({checker.name : result[1]})
                if result[0] == False:
                    responseCode = 500
            except Exception as e:
                response["checks"].append({checker.name : "Failed - check logs"})
                current_app.logger.exception(f"Check {checker.name} failed with an exception")
                responseCode = 500
        return response, responseCode

    def add_check(self, checker):
        self.checkers.append(checker)

class CheckerInterface:
    def check(self):
        pass

class FlaskRunningChecker(CheckerInterface):
    def __init__(self):
        self.name = "check_running"

    def check(self):
        if(current_app):
            return True, "OK"
        else:
            return False, "Fail"

class DbChecker(CheckerInterface):

    def __init__(self, db):
        self.db = db
        self.name = "check_db"

    def check(self):
        self.db.session.execute("SELECT 1")
        return True, "OK"
    