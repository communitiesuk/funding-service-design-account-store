"""
Tests the GET and POST functionality of our api.
"""
import sys
from tests.helpers import expected_data_within_response


class TestAccountsPost:
    def test_create_account_with_email(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we POST to the /accounts endpoint with a json payload of
            {
                "email_address": <email>
            }
        THEN a new account record is created with the given email

        """

        email = "person1@example.com"
        params = {"email_address": email}
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert "account_id" in response.json
        assert "azure_ad_subject_id" in response.json
        assert response.json["email_address"] == email

    def test_create_account_with_existing_account_email_fails(
        self, flask_test_client
    ):
        """
        GIVEN The flask test client
        WHEN we POST twice to the /accounts endpoint with a json payload of
            {
                "email_address": <email>
            }
        THEN the second post returns a 409 error

        """

        email = "person1@example.com"
        params = {"email_address": email}
        url = "/accounts"

        first_response = flask_test_client.post(url, json=params)

        assert first_response.status_code == 201

        second_response = flask_test_client.post(url, json=params)

        assert second_response.status_code == 409

    def test_create_account_with_email_and_azure_ad_subject_id(
        self, flask_test_client
    ):
        """
        GIVEN The flask test client
        WHEN we POST to the /accounts endpoint with a json payload of
            {
                "email_address": <email>,
                "azure_ad_subject_id": <azure_ad_subject_id>,
            }
        THEN a new account record is created with the given email
            and azure_ad_subject_id

        """

        email = "person1@example.com"
        azure_ad_subject_id = "abc_123"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert "account_id" in response.json
        assert "azure_ad_subject_id" in response.json
        assert response.json["email_address"] == email
        assert response.json["azure_ad_subject_id"] == azure_ad_subject_id

    def test_create_account_with_existing_azure_subject_id_fails(
        self, flask_test_client
    ):
        """
        GIVEN The flask test client
        WHEN we POST to the /accounts endpoint with a json payload of
            {
                "email_address": <email>,
                "azure_ad_subject_id": <existing_azure_ad_subject_id>,
            }
        THEN a new account record is created with the given email
            and azure_ad_subject_id

        """

        email1 = "person1@example.com"
        azure_ad_subject_id = "abc_123"
        params = {
            "email_address": email1,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        first_response = flask_test_client.post(url, json=params)

        assert first_response.status_code == 201

        email2 = "person2@example.com"
        params2 = {
            "email_address": email2,
            "azure_ad_subject_id": azure_ad_subject_id,
        }

        second_response = flask_test_client.post(url, json=params2)

        assert second_response.status_code == 409


class TestAccountsGet:
    def test_get_by_unique_columns(self, flask_test_client):
        """
        GIVEN an instance of our API
        WHEN we send a GET request to the /accounts endpoint
        WITH a query arg of either:
            email_address=<valid_account_email>
            account_id=<valid_account_id>
            azure_ad_subject_id=<azure_ad_subject_id>
        THEN a matching account record is returned with the correct params
        """
        # Create a valid record
        email = "person1@example.com"
        azure_ad_subject_id = "abc_123"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        account_id = response.json["account_id"]

        # Expected GET response
        expected_response_data = {
            "account_id": account_id,
            "email_address": email,
            "full_name": None,
            "azure_ad_subject_id": azure_ad_subject_id,
            "roles": [],
        }

        # Check expected response with email query arg
        email_arg = "email_address=" + email
        email_arg_url = "/accounts?" + email_arg
        expected_data_within_response(
            flask_test_client, email_arg_url, expected_response_data, 200
        )

        # Check expected response with account_id query arg
        account_id_arg = "account_id=" + account_id
        account_id_arg_url = "/accounts?" + account_id_arg
        expected_data_within_response(
            flask_test_client, account_id_arg_url, expected_response_data, 200
        )

        # Check expected response with azure_ad_subject_id query arg
        azure_ad_subject_id_arg = "azure_ad_subject_id=" + azure_ad_subject_id
        azure_ad_subject_id_arg_url = "/accounts?" + azure_ad_subject_id_arg
        expected_data_within_response(
            flask_test_client,
            azure_ad_subject_id_arg_url,
            expected_response_data,
            200,
        )

        # Check expected response with multiple valid query args
        all_args_url = "/accounts?" + "&".join(
            [email_arg, account_id_arg, azure_ad_subject_id_arg]
        )
        expected_data_within_response(
            flask_test_client, all_args_url, expected_response_data, 200
        )






    def test_get_bulk_by_account_ids(self, flask_test_client):
        """
        GIVEN an instance of our API
        WHEN we send a GET request to the /bulk-accounts endpoint
        WITH a query arg of multiple:
            account_id=<valid_account_id>
        THEN matching account records are returned with the correct params
        """
        account_ids = []
        expected_response_data = {}

        # Create a valid record
        records_to_create = [
            {
            "email" : "person1@example.com",
            "azure_ad_subject_id" : "abc_123",
            },
            {
            "email" : "person2@example.com",
            "azure_ad_subject_id" : "abc_234",

            }
        ]

        for record in records_to_create:
            params = {
                "email_address": record["email"],
                "azure_ad_subject_id": record["azure_ad_subject_id"],
            }
            url = "/accounts"

            response = flask_test_client.post(url, json=params)
            assert response.status_code == 201
            account_ids.append(response.json["account_id"])

            expected_response_data.update({
                response.json["account_id"]: {
                    "account_id": response.json["account_id"],
                    "azure_ad_subject_id": response.json["azure_ad_subject_id"],
                    "email_address": response.json["email_address"],
                    "full_name": None,
                    "roles": []
                }
            })
            
        # Check expected response with account_id query arg
        account_id_arg = "account_id="
        account_id_arg_url = "/bulk-accounts?" + account_id_arg

        count = 0
        for id in account_ids:
            if count < 1:
                account_id_arg_url += id
                count += 1
            else: account_id_arg_url += "&account_id=" + id

        expected_data_within_response(
            flask_test_client, account_id_arg_url, expected_response_data, 200
        )

    def test_get_by_mismatched_unique_columns_fails(self, flask_test_client):
        """
        GIVEN an instance of our API
        WHEN we send a GET request to the /accounts endpoint
        WITH a query arg of either:
            email_address=<invalid_account_email>
            account_id=<valid_account_id>
            azure_ad_subject_id=<azure_ad_subject_id>
        THEN a 404 is raised due to the mismatched email
        """
        # Create a valid record
        email = "person1@example.com"
        azure_ad_subject_id = "abc_123"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        account_id = response.json["account_id"]

        # Check expected response with mismatched query args
        wrong_email_arg = "email_address=wrong-email@example.com"
        account_id_arg = "account_id=" + account_id
        azure_ad_subject_id_arg = "azure_ad_subject_id=" + azure_ad_subject_id
        all_args_url = "/accounts?" + "&".join(
            [wrong_email_arg, account_id_arg, azure_ad_subject_id_arg]
        )
        response = flask_test_client.get(all_args_url)

        assert response.status_code == 404

    def test_get_to_non_existing_resource_returns_404(self, flask_test_client):

        email = "non_existant_email@example.com"
        url = "/accounts?email_address=" + email

        response = flask_test_client.get(url)

        assert response.status_code == 404


class TestAccountsPut:

    test_email_1 = "person1@example.com"
    test_email_2 = "person2@example.com"
    accounts_created = {}

    def test_update_full_name_role_and_azure_ad_subject_id(
        self, flask_test_client
    ):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of
            {
                "roles":"LEAD_ASSESSOR",
                "full_name": "Jane Doe",
                "azure_ad_subject_id": "abc_123",
            }
        THEN the account full_name, roles and azure_ad_subject_id are updated

        """
        email = "person1@example.com"
        params = {"email_address": email}
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == email

        account_id = response.json["account_id"]
        new_roles = ["ASSESSOR"]
        new_full_name = "Jane Doe"
        new_azure_ad_subject_id = "abc_123"
        params = {
            "roles": new_roles,
            "full_name": new_full_name,
            "azure_ad_subject_id": new_azure_ad_subject_id,
        }
        url = "/accounts/" + account_id

        expected_response_data = {
            "account_id": account_id,
            "email_address": email,
            "full_name": new_full_name,
            "azure_ad_subject_id": new_azure_ad_subject_id,
            "roles": new_roles,
        }

        expected_data_within_response(
            flask_test_client,
            url,
            expected_response_data,
            201,
            method="put",
            json=params,
        )

    def test_update_full_name_role_without_azure_ad_subject_id_fails(
        self, flask_test_client
    ):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of
            {
                "roles":"LEAD_ASSESSOR",
                "full_name": "Jane Doe",
            }
        THEN a bad request error is returned

        """
        email = "person1@example.com"
        params = {"email_address": email}
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == email

        account_id = response.json["account_id"]
        new_roles = ["ASSESSOR"]
        new_full_name = "Jane Doe"
        params = {
            "roles": new_roles,
            "full_name": new_full_name,
        }
        url = "/accounts/" + account_id

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 400
        assert (
            response.json.get("detail")
            == "'azure_ad_subject_id' is a required property"
        )

    def test_update_role_only(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of
        {
            "roles":"LEAD_ASSESSOR",
            "azure_ad_subject_id": "abc_123",
        }
        THEN the account role is updated

        """
        azure_ad_subject_id = "abc_123"
        email = "person1@example.com"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == email

        account_id = response.json["account_id"]
        new_roles = ["LEAD_ASSESSOR"]
        params = {
            "roles": new_roles,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts/" + account_id

        expected_response_data = {
            "account_id": account_id,
            "email_address": email,
            "full_name": None,
            "azure_ad_subject_id": azure_ad_subject_id,
            "roles": new_roles,
        }

        expected_data_within_response(
            flask_test_client,
            url,
            expected_response_data,
            201,
            method="put",
            json=params,
        )

    def test_update_role_with_non_existent_role_fails(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of
        {
            "roles":"BAD_ROLE",
            "azure_ad_subject_id": <existing_subject_id>,
        }
        THEN tan error is returned

        """
        azure_ad_subject_id = "abc_123"
        email = "person1@example.com"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)
        account_id = response.json["account_id"]
        bad_role = "BAD_ROLE"
        params = {
            "roles": [bad_role],
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts/" + account_id

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 401
        assert f"Role '{bad_role}' is not valid" in response.json.get("error")
