from json import dumps
from unittest.mock import ANY, Mock, patch
import flask


from healthcheck import Healthcheck

class TestHealthcheck:
    def testHealthChecksSetup(self):
        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)
        assert health.checks == [], "Checks not initialised"

    def testWithNoChecks(self):
        mock_app = Mock()
        health = Healthcheck(mock_app)
        expected_dict = {"checks":[]}

        result = health.healthcheck_view()
        assert result[0] == dumps(expected_dict), "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"

    def testWithChecksPassing_properMocks(self):
        mock_app = Mock()
        mock_app.logger.debug = Mock()
        health = Healthcheck(mock_app)
        expected_dict = {"checks":[{"check_a": "ok"}, {"check_b": "ok"}]}

        check_a =Mock()
        check_a.return_value = True, "ok"
        check_a.__name__ = "check_a"
        health.add_check(check_a)
        check_b =Mock()
        check_b.return_value = True, "ok"
        check_b.__name__ = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"
        # mock_app.logger.debug.assert_called()

    def testWithChecksPassing_appContext(self, flask_test_client):       
        expected_dict = {"checks":[{"check_running": "OK"}, {"check_db": "OK"}]}

        response = flask_test_client.get("/healthcheck")
        assert response.status_code == 200, "Unexpected status code"
        print(response.json)
        print(dumps(expected_dict))
        assert response.json == expected_dict, "Unexpected response body"