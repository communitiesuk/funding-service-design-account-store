"""
Tests the roles update functionality of our api.
"""


class TestRoles:
    test_email = "person@example.com"
    accounts_created = {test_email: "APPLICANT"}

    def test_create_account_returns_role(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we POST to the /accounts endpoint
        WITH a json payload of
            {
                "email: "person@example.com"
            }
        THEN the account is created with the correct role
        Args:
            flask_test_client: the test client
        """
        params = {
            "email_address": self.test_email
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == self.test_email
        assert response.json["role"] == "APPLICANT"
        self.accounts_created.update({
            self.test_email: response.json["account_id"]
        })

    def test_update_role(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of {"role":"LEAD_ASSESSOR"}
        THEN the account role is updated

        """

        new_role = "ASSESSOR"
        params = {
            "role": new_role
        }
        url = "/accounts/" + self.accounts_created.get(self.test_email)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201
        assert "email_address" in response.json.keys()
        assert "role" in response.json.keys()
        assert response.json["email_address"] == self.test_email
        assert response.json["role"] == new_role


    def test_update_role_with_non_existant_role_fails(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of {"role":"BAD_ROLE"}
        THEN the account role is updated

        """

        new_role = "BAD_ROLE"
        params = {
            "role": new_role
        }
        url = "/accounts/" + self.accounts_created.get(self.test_email)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 401
