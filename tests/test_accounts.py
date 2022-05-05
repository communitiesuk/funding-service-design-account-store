"""
Tests the GET and POST functionality of our api.
"""
import ast
from typing import Tuple

import pytest
from flask import request
from requests import PreparedRequest


@pytest.mark.usefixtures("client_class")
class TestAccounts:
    def test_new_post(self):

        status_code, response_data = self.post_email_and_return_data(
            "ram@harry-styles-fanclub.org"
        )

        assert status_code == 200

        assert "account_id" in response_data.keys()

        assert "applications" in response_data.keys()

        assert response_data["email_address"] == "ram@harry-styles-fanclub.org"

    def test_double_post_returns_409(self):

        params = {"email_address": "ram2@harry-styles-fanclub.org"}

        req = PreparedRequest()

        root_url = request.root_url

        url = root_url + "account"

        req.prepare_url(url, params)

        response1 = self.client.post(req.url)

        response2 = self.client.post(req.url)

        assert response1.status_code == 200
        assert response2.status_code == 409

    def test_get_methods_work(self):

        _, response_dict = self.post_email_and_return_data(
            "ram400@harry-styles-fanclub.org"
        )

        email = response_dict["email_address"]
        account_id = response_dict["account_id"]

        email_response_data = self.get_and_return_data(
            email_address=email
        ).data

        account_response_data = self.get_and_return_data(
            account_id=account_id
        ).data

        email_dict = ast.literal_eval(email_response_data.decode("utf-8"))

        account_dict = ast.literal_eval(account_response_data.decode("utf-8"))

        assert email_response_data == account_response_data

        assert email_dict["account_id"] == account_id

        assert account_dict["email_address"] == email

        assert (
            account_dict["email_address"]
            == email_dict["email_address"]
            == "ram400@harry-styles-fanclub.org"
        )

    def get_to_non_existing_resource_returns_204(self):

        response = self.get_and_return_data(
            email_address="ram40000@harry-stylees-fanclub.org"
        )

        assert response.status_code == 204

    def get_and_return_data(self, email_address=None, account_id=None):

        if email_address is None and account_id is None:

            raise TypeError("Atleast 1 argument must be given.")

        if email_address is not None and account_id is not None:

            raise TypeError("Only one kwarg can be given.")

        raw_params = {"email_address": email_address, "account_id": account_id}

        params = {k: v for k, v in raw_params.items() if v is not None}

        req = PreparedRequest()

        root_url = request.root_url

        url = root_url + "account"

        req.prepare_url(url, params)

        response = self.client.get(req.url)

        return response

    def post_email_and_return_data(
        self, email_address: str
    ) -> Tuple[int, dict]:

        params = {"email_address": email_address}

        req = PreparedRequest()

        root_url = request.root_url

        url = root_url + "account"

        req.prepare_url(url, params)

        response = self.client.post(req.url)

        post_response_data = response.data

        # turns the bytestring into a python dictionary.
        response_dict = ast.literal_eval(post_response_data.decode("utf-8"))

        return response.status_code, response_dict
