from unittest.mock import ANY, Mock, patch
from sqlalchemy.exc import OperationalError


from healthcheck import FlaskRunningChecker, Healthcheck

class TestHealthcheck():
    def testHealthChecksSetup(self):
        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)
        assert health.checkers == [], "Checks not initialised"

    def testWithNoChecks(self):
        mock_app = Mock()
        health = Healthcheck(mock_app)
        mock_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks":[]}

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"

    def testWithChecksPassing_mocks(self, flask_test_client):
        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks":[{"check_a": "ok"}, {"check_b": "ok"}]}

        check_a =Mock()
        check_a.check.return_value = True, "ok"
        check_a.name = "check_a"
        health.add_check(check_a)
        check_b =Mock()
        check_b.check.return_value = True, "ok"
        check_b.name = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 200, "Unexpected status code"

    def testWithChecksFailing_mocks(self, flask_test_client):

        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks":[{"check_a": "fail"}, {"check_b": "ok"}]}

        check_a =Mock()
        check_a.check.return_value = False, "fail"
        check_a.name = "check_a"
        health.add_check(check_a)
        check_b =Mock()
        check_b.check.return_value = True, "ok"
        check_b.name = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 500, "Unexpected status code"

    def testWithChecksException_mocks(self, flask_test_client):

        test_app = Mock()
        health = Healthcheck(test_app)
        test_app.add_url_rule.assert_called_with("/healthcheck", view_func=ANY)

        expected_dict = {"checks":[{"check_a": "fail"}, {"check_b": "Failed - check logs"}]}

        check_a =Mock()
        check_a.check.return_value = False, "fail"
        check_a.name = "check_a"
        health.add_check(check_a)
        check_b =Mock()
        check_b.check.side_effect = OperationalError
        check_b.name = "check_b"
        health.add_check(check_b)

        result = health.healthcheck_view()
        assert result[0] == expected_dict, "Unexpected response body"
        assert result[1] == 500, "Unexpected status code"

    def testWithRealChecksPassing(self, flask_test_client):       
        expected_dict = {"checks":[{"check_running": "OK"}, {"check_db": "OK"}]}

        response = flask_test_client.get("/healthcheck")
        assert response.status_code == 200, "Unexpected status code"
        assert response.json == expected_dict, "Unexpected response body"

    def testRunningCheck_pass(self, flask_test_client):
        result = FlaskRunningChecker().check()
        assert result[0] == True, "Unexpected check result"
        assert result[1] == "OK", "Unexpected check message"

    # @patch("flask.current_app")
    # def testRunningCheck_fail(self, flask_test_client):
    #     result = Healthcheck.check_running()
    #     assert result[0] == False, "Unexpected check result"
    #     assert result[1] == "Fail", "Unexpected check message"