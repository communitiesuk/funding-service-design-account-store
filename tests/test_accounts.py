"""
Tests the GET and POST functionality of our api.
"""
import ast

import pytest
from flask import request
from requests import PreparedRequest
from tests.helpers import get_and_return_data
from tests.helpers import post_email_and_return_data


@pytest.mark.usefixtures("client_class")
class TestAccounts:
    def test_new_post(self):
        """test_new_post Creates a random email address and posts it
         to the account store,then checks that the email address
        exists in the account store.

        GIVEN The flask test client
        WHEN an email is submitted
        THEN we expect that the email exists in the account store.

        """

        status_code, response_data = post_email_and_return_data(
            self.client, "test@delete_me.org"
        )

        assert status_code == 200
        assert "account_id" in response_data.keys()
        assert "applications" in response_data.keys()
        assert response_data["email_address"] == "test@delete_me.org"

    def test_double_post_returns_409(self):

        params = {"email_address": "test2@delete_me.org"}

        req = PreparedRequest()
        root_url = request.root_url
        url = root_url + "account"
        req.prepare_url(url, params)

        response1 = self.client.post(req.url)
        response2 = self.client.post(req.url)

        assert response1.status_code == 200
        assert response2.status_code == 409

    def test_get_methods_work(self):
        """
        GIVEN An instance of our API
        WHEN Several get requests of
         various VALID forms are made
        THEN we except them all to yield a
        200 status code back (they succeed).
        """

        _, response_dict = post_email_and_return_data(
            self.client, email_address="test3@delete_me.org"
        )

        email = response_dict["email_address"]
        account_id = response_dict["account_id"]

        email_response_data = get_and_return_data(
            self.client, email_address=email
        ).data
        account_response_data = get_and_return_data(
            self.client, account_id=account_id
        ).data
        email_dict = ast.literal_eval(email_response_data.decode("utf-8"))
        account_dict = ast.literal_eval(account_response_data.decode("utf-8"))

        assert email_response_data == account_response_data
        assert email_dict["account_id"] == account_id
        assert account_dict["email_address"] == email
        assert (
            account_dict["email_address"]
            == email_dict["email_address"]
            == "test3@delete_me.org"
        )

    def test_get_to_non_existing_resource_returns_204(self):

        response = get_and_return_data(
            self.client, email_address="dfgdfjg@sdjlkjsf.org"
        )

        assert response.status_code == 204
