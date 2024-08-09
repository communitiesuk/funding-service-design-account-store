"""
Tests the GET and POST functionality of our api.
"""

import uuid

import pytest

from tests.conftest import test_user_1
from tests.conftest import test_user_2
from tests.conftest import test_user_to_update
from tests.helpers import expected_data_within_response


class TestAccountsPost:
    def test_create_account_with_email(self, flask_test_client, clear_test_data):
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
        assert "account_id" in response.json()
        assert "azure_ad_subject_id" in response.json()
        assert response.json()["email_address"] == email

    def test_create_account_with_existing_account_email_fails(self, flask_test_client, clear_test_data):
        """
        GIVEN The flask test client
        WHEN we POST twice to the /accounts endpoint with a json payload of
            {
                "email_address": <email>
            }
        THEN the second post returns a 409 error

        """

        email = "person2@example.com"
        params = {"email_address": email}
        url = "/accounts"

        first_response = flask_test_client.post(url, json=params)

        assert first_response.status_code == 201

        second_response = flask_test_client.post(url, json=params)

        assert second_response.status_code == 409

    def test_create_account_with_email_and_azure_ad_subject_id(self, flask_test_client, clear_test_data):
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

        email = "person3@example.com"
        azure_ad_subject_id = "abc_123"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert "account_id" in response.json()
        assert "azure_ad_subject_id" in response.json()
        assert response.json()["email_address"] == email
        assert response.json()["azure_ad_subject_id"] == azure_ad_subject_id

    def test_create_account_with_existing_azure_subject_id_fails(self, flask_test_client, clear_test_data):
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

        email1 = "person4@example.com"
        azure_ad_subject_id = "abc_456"
        params = {
            "email_address": email1,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        url = "/accounts"

        first_response = flask_test_client.post(url, json=params)

        assert first_response.status_code == 201

        email2 = "person4@example.com"
        params2 = {
            "email_address": email2,
            "azure_ad_subject_id": azure_ad_subject_id,
        }

        second_response = flask_test_client.post(url, json=params2)

        assert second_response.status_code == 409


class TestAccountsGet:
    @pytest.mark.parametrize(
        "url_params_map, expected_status_code, expected_user_result",
        [
            ({"email_address": "seeded_user_1@example.com"}, 200, test_user_1),
            ({"account_id": test_user_1["account_id"]}, 200, test_user_1),
            ({"azure_ad_subject_id": "subject_id_1"}, 200, test_user_1),
            (
                {
                    "azure_ad_subject_id": "subject_id_1",
                    "account_id": test_user_1["account_id"],
                    "email_address": "seeded_user_1@example.com",
                },
                200,
                test_user_1,
            ),
            (
                {
                    "email_address": "does_not_exist@example.com",
                },
                404,
                None,
            ),
            (
                {
                    "azure_ad_subject_id": "subject_id_1",
                    "email_address": "seeded_user_2@example.com",
                },
                404,
                None,
            ),
        ],
    )
    def test_get_user(
        self,
        flask_test_client,
        seed_test_data,
        url_params_map,
        expected_status_code,
        expected_user_result,
    ):
        url = "/accounts?"
        for key in url_params_map.keys():
            url += f"{key}={url_params_map[key]}&"
        response = flask_test_client.get(url)
        assert response.status_code == expected_status_code
        assert response.json()
        if expected_user_result:
            assert response.json()["email_address"] == expected_user_result["email"]
            assert response.json()["account_id"] == str(expected_user_result["account_id"])

    @pytest.mark.parametrize(
        "account_ids, expected_status_code, expected_user_results",
        [
            (
                [test_user_1["account_id"], test_user_2["account_id"]],
                200,
                [test_user_1, test_user_2],
            ),
            ([test_user_1["account_id"]], 200, [test_user_1]),
            (
                [test_user_1["account_id"], "ca69e0c8-0000-0000-0000-177038a16e56"],
                200,
                [test_user_1],
            ),
            (["ca69e0c8-0000-0000-0000-177038a16e56"], 200, []),
        ],
    )
    def test_get_bulk_accounts(
        self,
        flask_test_client,
        seed_test_data,
        account_ids,
        expected_status_code,
        expected_user_results,
    ):
        url = "/bulk-accounts?"
        for id in account_ids:
            url += f"account_id={id}&"
        response = flask_test_client.get(url)
        assert response.status_code == expected_status_code
        assert response.json() is not None
        assert len(response.json()) == len(expected_user_results)
        for expected_user in expected_user_results:
            user_in_response = response.json().get(str(expected_user["account_id"]))
            assert user_in_response
            assert user_in_response["email_address"] == expected_user["email"]


class TestAccountsPut:
    test_email_1 = "person1@example.com"
    test_email_2 = "person2@example.com"
    accounts_created = {}

    def test_update_full_name_role_and_azure_ad_subject_id(self, flask_test_client, clear_test_data, seed_test_data):
        account_id = str(test_user_to_update["account_id"])
        new_roles = ["COF_ASSESSOR"]
        new_full_name = "Jane Doe"
        new_azure_ad_subject_id = "subject_id_x"
        params = {
            "roles": new_roles,
            "full_name": new_full_name,
            "azure_ad_subject_id": new_azure_ad_subject_id,
        }
        url = "/accounts/" + account_id

        expected_response_data = {
            "account_id": account_id,
            "email_address": "seeded_user_x@example.com",
            "full_name": new_full_name,
            "azure_ad_subject_id": new_azure_ad_subject_id,
            "roles": ["COF_ASSESSOR"],
            "highest_role_map": {"COF": "ASSESSOR"},
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
        self, flask_test_client, clear_test_data, seed_test_data
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
        account_id = str(test_user_to_update["account_id"])
        new_roles = ["LEAD_ASSESSOR"]
        new_full_name = "Jane Doe 2"
        params = {
            "roles": new_roles,
            "full_name": new_full_name,
        }
        url = "/accounts/" + account_id

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 400
        assert response.json().get("detail") == "'azure_ad_subject_id' is a required property"

    def test_update_role_only(self, flask_test_client, clear_test_data, seed_test_data):
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

        account_id = str(test_user_to_update["account_id"])
        new_roles = ["COF_COMMENTER"]
        params = {
            "roles": new_roles,
            "azure_ad_subject_id": "subject_id_x",
        }
        url = "/accounts/" + account_id

        response = flask_test_client.put(url, json=params)
        assert response.status_code == 201

        assert response.json()["account_id"] == account_id
        assert response.json()["roles"] == ["COF_COMMENTER"]

    def test_update_role_with_non_existent_role_allows(self, flask_test_client, clear_test_data, seed_test_data):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of
        {
            "roles":"NON_EXISTENT_ROLE",
            "azure_ad_subject_id": <existing_subject_id>,
        }
        THEN it is allowed

        Each application should check roles for an account
        before allowing access.

        """

        account_id = str(test_user_to_update["account_id"])
        new_roles = ["NON_EXISTENT_ROLE"]
        params = {
            "roles": new_roles,
            "azure_ad_subject_id": "subject_id_x",
        }
        url = "/accounts/" + account_id

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201


class TestGetAccountsForFund:
    @pytest.mark.user_config(
        [
            {
                "email": "assessor@example.com",
                "subject_id": "1",
                "account_id": uuid.uuid4(),
                "roles": ["COF_ASSESSOR_R1"],
            },
            {
                "email": "commenter@example.com",
                "subject_id": "2",
                "account_id": uuid.uuid4(),
                "roles": ["COF_COMMENTER_R1"],
            },
            {
                "email": "otherround@example.com",
                "subject_id": "3",
                "account_id": uuid.uuid4(),
                "roles": ["COF_COMMENTER_R2"],
            },
            {
                "email": "otherfund@example.com",
                "subject_id": "4",
                "account_id": uuid.uuid4(),
                "roles": ["HSRA_ASSESSOR_R1"],
            },
        ]
    )
    def test_successful_retrieval(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.get("/accounts/fund/COF")
        assert response.status_code == 200
        assert len(response.json()) == 3

    @pytest.mark.user_config(
        [
            {
                "email": "assessor@example.com",
                "subject_id": "1",
                "account_id": uuid.uuid4(),
                "roles": ["COF_ASSESSOR_R1"],
            },
            {
                "email": "commenter@example.com",
                "subject_id": "2",
                "account_id": uuid.uuid4(),
                "roles": ["COF_COMMENTER_R1"],
            },
        ]
    )
    def test_assessors_only(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.get("/accounts/fund/COF?include_assessors=true&include_commenters=false")
        assert response.status_code == 200
        assert len(response.json()) == 1  # Only the assessor should be returned
        assert all("ASSESSOR" in role for role in response.json()[0]["roles"])

    @pytest.mark.user_config(
        [
            {
                "email": "assessor@example.com",
                "subject_id": "1",
                "account_id": uuid.uuid4(),
                "roles": ["COF_ASSESSOR_R1"],
            },
            {
                "email": "commenter@example.com",
                "subject_id": "2",
                "account_id": uuid.uuid4(),
                "roles": ["COF_COMMENTER_R1"],
            },
        ]
    )
    def test_commenters_only(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.get("/accounts/fund/COF?include_assessors=false&include_commenters=true")
        assert response.status_code == 200
        assert len(response.json()) == 1  # Only the commenter should be returned
        assert all("COMMENTER" in role for role in response.json()[0]["roles"])

    @pytest.mark.user_config([])  # No users configured
    def test_no_matching_accounts(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.get("/accounts/fund/unknownfund")
        assert response.status_code == 404
        assert response.json() == {"error": "No matching accounts found"}

    @pytest.mark.user_config(
        [
            {
                "email": "both@example.com",
                "subject_id": "3",
                "account_id": uuid.uuid4(),
                "roles": ["COF_ASSESSOR_R1", "COF_COMMENTER_R1"],
            }
        ]
    )
    def test_bad_request(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.get("/accounts/fund/COF?include_assessors=false&include_commenters=false")
        assert response.status_code == 400
        assert response.json() == {"error": "One of include_assessors or include_commenters must be true"}


@pytest.mark.user_config(
    [
        {
            "email": "assessor-1@example.com",
            "subject_id": "1",
            "account_id": uuid.uuid4(),
            "roles": ["COF_ASSESSOR_R1"],
        },
        {
            "email": "assessor-2@communities.gov.uk",
            "subject_id": "2",
            "account_id": uuid.uuid4(),
            "roles": ["COF_COMMENTER_R2"],
        },
        {
            "email": "assessor-3@communities.gov.uk",
            "subject_id": "3",
            "account_id": uuid.uuid4(),
            "roles": ["COF_ASSESSOR_R3", "COF_COMMENTER_R4"],
        },
        {
            "email": "section-151@communities.gov.uk",
            "subject_id": "4",
            "account_id": uuid.uuid4(),
            "roles": ["SECTION_151"],
        },
    ]
)
class TestAccountSearch:
    def test_search_all_accounts_no_json_body(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search")

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 4

    def test_search_all_accounts_empty_json_body(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 4

    def test_search_all_accounts_by_email_domain(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"email_domain": "example.com"})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 1
        assert accounts[0]["email_address"] == "assessor-1@example.com"

    def test_search_all_accounts_by_roles(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"roles": ["SECTION_151"]})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 1
        assert accounts[0]["email_address"] == "section-151@communities.gov.uk"

    def test_search_all_accounts_by_multiple_roles(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"roles": ["COF_ASSESSOR_R1", "COF_COMMENTER_R2"]})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 2
        assert accounts[0]["email_address"] == "assessor-1@example.com"
        assert accounts[1]["email_address"] == "assessor-2@communities.gov.uk"

    def test_search_all_accounts_by_roles_case_sensitive(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"roles": ["section_151"]})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 0

    def test_search_all_accounts_by_partial_roles(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"partial_roles": ["COMMENTER"]})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 2
        assert accounts[0]["email_address"] == "assessor-2@communities.gov.uk"
        assert accounts[1]["email_address"] == "assessor-3@communities.gov.uk"

    def test_search_all_accounts_by_partial_roles_case_sensitive(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"roles": ["commenter"]})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 0

    def test_search_all_accounts_by_multiple_partial_roles(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"partial_roles": ["R1", "COMMENTER"]})

        assert response.status_code == 200

        accounts = response.json()
        assert len(accounts) == 3
        assert accounts[0]["email_address"] == "assessor-1@example.com"
        assert accounts[1]["email_address"] == "assessor-2@communities.gov.uk"
        assert accounts[2]["email_address"] == "assessor-3@communities.gov.uk"

    def test_search_all_accounts_additional_properties_blocked(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"blah": False})

        assert response.status_code == 400

    def test_search_cannot_filter_on_roles_and_partial_roles_together(self, flask_test_client, seed_test_data_fn):
        response = flask_test_client.post("/accounts/search", json={"roles": ["SECTION_151"], "partial_roles": ["R1"]})

        assert response.status_code == 400
