from typing import List
from typing import Tuple

import sqlalchemy
from connexion import NoContent
from db import db
from db.models.account import Account
from db.models.role import Role
from db.models.role import RoleType
from sqlalchemy import delete


def check_account_exists_then_return(
    account_id: str, as_json: bool = True
) -> Tuple[dict, int]:
    """check_exists_then_get Checks that the key exists in the db
     and returns a value if so.

    Args:
        key (str): A key we would like the query in our db.

    Returns:
        A tuple with content and a status code.
    """

    try:
        account = (
            db.session.query(Account).filter(Account.id == account_id).one()
        )

        if as_json:
            return {
                "account_id": account.id,
                "email_address": account.email,
                "roles": account.serialize["roles"],
            }, 200
        else:
            return account
    except sqlalchemy.exc.NoResultFound:
        return NoContent, 404


def update_account(account_id: str, roles: List[str]) -> Tuple[dict, int]:
    """
    Updates an account rols
    Args:
        account_id (str): The account id
        roles (List[str]): A list of roles to set

    Returns:
        A tuple with account status as json and a status code.

    """
    # Check account exists
    try:
        account = (
            db.session.query(Account).filter(Account.id == account_id).one()
        )
    except sqlalchemy.exc.NoResultFound:
        return NoContent, 404
    # Check all roles are valid
    for role in roles:
        try:
            RoleType[role.upper()]
        except KeyError:
            return {"error": f"Role '{role}' is not valid"}, 401
    # Delete existing roles
    stmnt = delete(Role).where(Role.account_id == account_id)
    db.session.execute(stmnt)

    # Update current roles
    current_roles = []
    for role in roles:
        current_role = Role()
        current_role.account_id = account_id
        current_role.role = RoleType[role.upper()]
        current_roles.append(current_role)

    db.session.add_all(current_roles)
    db.session.commit()

    account = db.session.query(Account).filter(Account.id == account_id).one()

    return {
        "account_id": account.id,
        "email_address": account.email,
        "roles": account.serialize["roles"],
    }, 201


def get_account_data_by_email(
    email: str, as_json: bool = True
) -> Tuple[dict, int]:
    """get_data_by_email Allows you to fetch account by its email.

    Args:
        email (str): An email given a str.

    Returns:
        A tuple with content and a status code.
    """

    try:
        account = (
            db.session.query(Account).filter(Account.email == email).one()
        )
        account_id = account.id
    except sqlalchemy.exc.NoResultFound:
        return NoContent, 404

    return check_account_exists_then_return(account_id, as_json)
