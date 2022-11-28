"""
Tests the roles update functionality of our api.
"""


class TestRoles:
    test_email_1 = "person1@example.com"
    test_email_2 = "person2@example.com"
    accounts_created = {}

    def test_update_role(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of {"role":"LEAD_ASSESSOR"}
        THEN the account role is updated

        """
        params = {"email_address": self.test_email_1}
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == self.test_email_1
        self.accounts_created.update(
            {self.test_email_1: response.json["account_id"]}
        )

        new_roles = ["ASSESSOR"]
        params = {"roles": new_roles}
        url = "/accounts/" + self.accounts_created.get(self.test_email_1)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201
        assert "email_address" in response.json.keys()
        assert "roles" in response.json.keys()
        assert response.json["email_address"] == self.test_email_1
        assert response.json["roles"] == new_roles

    def test_update_role_with_non_existent_role_fails(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of {"role":"BAD_ROLE"}
        THEN tan error is returned

        """
        new_roles = ["BAD_ROLE"]
        params = {"roles": new_roles}
        url = "/accounts/" + self.accounts_created.get(self.test_email_1)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 401
