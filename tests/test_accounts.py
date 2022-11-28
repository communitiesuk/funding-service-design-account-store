"""
Tests the GET and POST functionality of our api.
"""
from tests.helpers import get_and_return_data
from tests.helpers import post_email_and_return_data


class TestAccountsPost:
    def test_new_post(self, flask_test_client):
        """test_new_post Creates a random email address and posts it
         to the account store,then checks that the email address
        exists in the account store.

        GIVEN The flask test client
        WHEN an email is submitted
        THEN we expect that the email exists in the account store.

        """

        status_code, response_data = post_email_and_return_data(
            flask_test_client, "test@delete_me.org"
        )

        assert status_code == 201
        assert "account_id" in response_data.keys()
        assert response_data["email_address"] == "test@delete_me.org"

    def test_double_post_returns_409(self, flask_test_client):

        params = {"email_address": "test2@delete_me.org"}

        url = "/accounts"

        response1 = flask_test_client.post(url, json=params)
        response2 = flask_test_client.post(url, json=params)

        assert response1.status_code == 201
        assert response2.status_code == 409


class TestAccountsGet:
    def test_get_methods_work(self, flask_test_client):
        """
        GIVEN An instance of our API
        WHEN Several get requests of
         various VALID forms are made
        THEN we except them all to yield a
        200 status code back (they succeed).
        """

        _, response_dict = post_email_and_return_data(
            flask_test_client, email_address="test3@delete_me.org"
        )

        email = response_dict["email_address"]
        account_id = response_dict["account_id"]

        email_response_data = get_and_return_data(
            flask_test_client, email_address=email
        )
        account_response_data = get_and_return_data(
            flask_test_client, account_id=account_id
        )

        email_dict = email_response_data.json
        account_dict = account_response_data.json

        assert email_response_data.json == account_response_data.json
        assert email_dict["account_id"] == account_id
        assert account_dict["email_address"] == email
        assert (
            account_dict["email_address"]
            == email_dict["email_address"]
            == "test3@delete_me.org"
        )

    def test_get_to_non_existing_resource_returns_404(self, flask_test_client):

        response = get_and_return_data(
            flask_test_client, email_address="dfgdfjg@sdjlkjsf.org"
        )

        assert response.status_code == 404


class TestAccountsPut:

    test_email_1 = "person1@example.com"
    test_email_2 = "person2@example.com"
    accounts_created = {}

    def test_update_full_name_and_role(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of
            {
                "role":"LEAD_ASSESSOR",
                "full_name": "Jane Doe",
            }
        THEN the account full_name is updated

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
        new_full_name = "Jane Doe"
        params = {"roles": new_roles, "full_name": new_full_name}
        url = "/accounts/" + self.accounts_created.get(self.test_email_1)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201
        assert "email_address" in response.json.keys()
        assert "full_name" in response.json.keys()
        assert "roles" in response.json.keys()
        assert response.json["email_address"] == self.test_email_1
        assert response.json["full_name"] == new_full_name
        assert response.json["roles"] == new_roles

    def test_update_role_only(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of {"role":"LEAD_ASSESSOR"}
        THEN the account role is updated

        """
        params = {"email_address": self.test_email_2}
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == self.test_email_2
        self.accounts_created.update(
            {self.test_email_2: response.json["account_id"]}
        )

        new_roles = ["LEAD_ASSESSOR"]
        params = {"roles": new_roles}
        url = "/accounts/" + self.accounts_created.get(self.test_email_2)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201
        assert "email_address" in response.json.keys()
        assert "roles" in response.json.keys()
        assert response.json["email_address"] == self.test_email_2
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
