"""
Contains test configuration.
"""

from uuid import uuid4

import pytest

from app import create_app
from db.models.account import Account
from db.models.role import Role

pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]


@pytest.fixture(scope="session")
def app():
    app = create_app()
    yield app.app


@pytest.fixture(scope="function")
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().test_client() as test_client:
        yield test_client


test_user_1 = {
    "email": "seeded_user_1@example.com",
    "subject_id": "subject_id_1",
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}
test_user_2 = {
    "email": "seeded_user_2@example.com",
    "subject_id": "subject_id_2",
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}
test_user_to_update = {
    "email": "seeded_user_x@example.com",
    "subject_id": "subject_id_x",
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}
test_user_2_to_update = {
    "email": "seeded_user_y@example.com",
    "subject_id": None,
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}


def create_user_with_roles(user_config, db):
    new_account = Account(
        email=user_config["email"],
        azure_ad_subject_id=user_config["subject_id"],
        id=user_config["account_id"],
    )
    db.session.add(new_account)
    db.session.commit()

    roles_to_add = []
    for r in user_config["roles"]:
        role = Role(account_id=user_config["account_id"], role=r)
        roles_to_add.append(role)
    db.session.add_all(roles_to_add)

    db.session.commit()


@pytest.fixture(scope="session")
def seed_test_data(request, app, clear_test_data, _db):
    marker = request.node.get_closest_marker("user_config")
    if not marker:
        users_to_create = [test_user_1, test_user_2, test_user_to_update, test_user_2_to_update]
    else:
        users_to_create = marker.args[0]
    for user in users_to_create:
        create_user_with_roles(user, _db)
    yield users_to_create


@pytest.fixture(scope="function")
def seed_test_data_fn(request, app, clear_test_data, _db):
    marker = request.node.get_closest_marker("user_config")
    if not marker:
        users_to_create = [test_user_1, test_user_2, test_user_to_update, test_user_2_to_update]
    else:
        users_to_create = marker.args[0]
    for user in users_to_create:
        create_user_with_roles(user, _db)
    yield users_to_create
    Role.query.delete()
    Account.query.delete()
    _db.session.commit()
