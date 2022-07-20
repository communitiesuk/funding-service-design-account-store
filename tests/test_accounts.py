"""
Tests the GET and POST functionality of our api.
"""
import json

from tests.helpers import get_and_return_data
from tests.helpers import post_email_and_return_data


class TestAccounts:
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
        assert "applications" in response_data.keys()
        assert response_data["email_address"] == "test@delete_me.org"

    def test_double_post_returns_409(self, flask_test_client):

        params = {"email_address": "test2@delete_me.org"}

        url = "/accounts"

        response1 = flask_test_client.post(url, json=params)
        response2 = flask_test_client.post(url, json=params)

        assert response1.status_code == 201
        assert response2.status_code == 409

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
        ).json
        account_response_data = get_and_return_data(
            flask_test_client, account_id=account_id
        ).data
        email_dict = json.load(email_response_data)
        account_dict = json.load(account_response_data)

        assert email_response_data == account_response_data
        assert email_dict["account_id"] == account_id
        assert account_dict["email_address"] == email
        assert (
            account_dict["email_address"]
            == email_dict["email_address"]
            == "test3@delete_me.org"
        )

    def test_get_to_non_existing_resource_returns_204(self, flask_test_client):

        response = get_and_return_data(
            flask_test_client, email_address="dfgdfjg@sdjlkjsf.org"
        )

        assert response.status_code == 404
