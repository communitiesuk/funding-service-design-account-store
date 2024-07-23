class TestHealthcheck:
    def testHealthcheckRoute(self, flask_test_client):
        expected_dict = {
            "checks": [{"check_flask_running": "OK"}, {"check_db": "OK"}],
            "version": "123123",
        }

        response = flask_test_client.get("/healthcheck")
        assert response.status_code == 200, "Unexpected status code"
        assert response.json() == expected_dict, "Unexpected response body"
