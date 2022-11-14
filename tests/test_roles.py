"""
Tests the roles update functionality of our api.
"""
from app import update_account_roles_cli


class TestRoles:
    test_email_1 = "person1@example.com"
    test_email_2 = "person2@example.com"
    accounts_created = {test_email_1: "APPLICANT"}

    def test_create_account_sets_role(self, flask_test_client):
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
            "email_address": self.test_email_1
        }
        url = "/accounts"

        response = flask_test_client.post(url, json=params)

        assert response.status_code == 201
        assert response.json["email_address"] == self.test_email_1
        assert response.json["role"] == "APPLICANT"
        self.accounts_created.update({
            self.test_email_1: response.json["account_id"]
        })

        # Get account to check role is set
        get_url = "/accounts?"
        get_response = flask_test_client.get(get_url + f"email_address={self.test_email_1}")
        assert get_response.status_code == 200
        assert get_response.json.get("role") == "APPLICANT"

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
        url = "/accounts/" + self.accounts_created.get(self.test_email_1)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201
        assert "email_address" in response.json.keys()
        assert "role" in response.json.keys()
        assert response.json["email_address"] == self.test_email_1
        assert response.json["role"] == new_role

    def test_update_role_with_non_existent_role_fails(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/{account_id} endpoint
        WITH a json payload of {"role":"BAD_ROLE"}
        THEN tan error is returned

        """
        new_role = "BAD_ROLE"
        params = {
            "role": new_role
        }
        url = "/accounts/" + self.accounts_created.get(self.test_email_1)

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 401

    def test_bulk_update_roles_successfully_updates_roles(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/update-roles endpoint
        WITH a json payload of {"a@example.com":"ADMIN"}
        THEN the account role is updated

        """
        # Create additional account
        create_account_url = "/accounts"
        create_response = flask_test_client.post(create_account_url, json={
            "email_address": self.test_email_2
        })
        self.accounts_created.update({
            self.test_email_1: create_response.json["account_id"]
        })

        # Update roles
        new_role_1 = "ADMIN"
        new_role_2 = "LEAD_ASSESSOR"
        params = {
            "roles": {
                self.test_email_1: new_role_1,
                self.test_email_2: new_role_2
            }
        }
        url = "/accounts/update-roles"

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 201
        assert response.json.get(self.test_email_1) == new_role_1
        assert response.json.get(self.test_email_2) == new_role_2

        # Get account to check role is set
        get_url = "/accounts?"
        get_response = flask_test_client.get(get_url+ f"email_address={self.test_email_1}")
        assert get_response.status_code == 200
        assert get_response.json.get("role") == new_role_1

        get_response = flask_test_client.get(get_url+f"email_address={self.test_email_2}")
        assert get_response.status_code == 200
        assert get_response.json.get("role") == new_role_2

    def test_bulk_update_role_with_non_existent_role_fails(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/update-roles endpoint
        WITH a json payload of {"a@example.com":"BAD_ROLE"}
        THEN the account role is updated

        """

        bad_email = "a@example.com"
        new_role = "BAD_ROLE"
        params = {
            "roles": {
                bad_email: new_role
            }
        }
        url = "/accounts/update-roles"

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 401

    def test_bulk_update_role_with_non_existent_email_fails(self, flask_test_client):
        """
        GIVEN The flask test client
        WHEN we PUT to the /accounts/update-roles endpoint
        WITH a json payload of {"a@bad-email.com":"ASSESSOR"}
        THEN the account role is updated

        """

        bad_email = "a@bad-email.com"
        new_role = "ASSESSOR"
        params = {
            "roles": {
                bad_email: new_role
            }
        }
        url = "/accounts/update-roles"

        response = flask_test_client.put(url, json=params)

        assert response.status_code == 401

    def test_cli_bulk_update_roles_successfully_updates_roles(self, mocker, app, flask_test_client):
        """
        GIVEN The flask app
        WHEN we run "flask update-account-roles"
        WITH a Config.ASSESSMENT_PROCESS_ROLES var of {"person2@example.com":"ADMIN"}
        THEN the account role is updated

        """
        runner = app.test_cli_runner()

        mocker.patch("config.Config.ASSESSMENT_PROCESS_ROLES", '{"person2@example.com":"ADMIN"}')
        result = runner.invoke(update_account_roles_cli)
        assert 'ROLES UPDATED' in result.output
        assert 'pers****le.com - ADMIN' in result.output

        # Get account to check role is set
        get_url = "/accounts?"
        get_response = flask_test_client.get(get_url + f"email_address=person2@example.com")
        assert get_response.status_code == 200
        assert get_response.json.get("role") == "ADMIN"

    def test_cli_bulk_update_roles_no_roles_message(self, mocker, app, flask_test_client):
        """
        GIVEN The flask app
        WHEN we run "flask update-account-roles"
        WITH a Config.ASSESSMENT_PROCESS_ROLES var of {}
        THEN a NO ROLES is shown

        """
        runner = app.test_cli_runner()

        mocker.patch("config.Config.ASSESSMENT_PROCESS_ROLES", '{}')
        result = runner.invoke(update_account_roles_cli)
        assert 'NO ROLES TO UPDATE' in result.output

    def test_cli_bulk_update_roles_error_messages(self, mocker, app, flask_test_client):
        """
        GIVEN The flask app
        WHEN we run "flask update-account-roles"
        WITH a Config.ASSESSMENT_PROCESS_ROLES var of {}
        THEN an error message is shown

        """
        runner = app.test_cli_runner()

        mocker.patch("config.Config.ASSESSMENT_PROCESS_ROLES", '{"a@bad-email.com":"ASSESSOR"}')
        result = runner.invoke(update_account_roles_cli)
        assert 'ERROR: ROLES UPDATE FAILED' in result.output
