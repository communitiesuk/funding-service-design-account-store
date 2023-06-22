"""
Contains the functions directly used by the openapi spec.
"""
from typing import Dict
from typing import Tuple

import sqlalchemy
from db import db
from db.models.account import Account
from db.models.role import Role
from db.schemas.account import AccountSchema
from flask import current_app
from flask import request
from sqlalchemy import delete
from sqlalchemy import or_
from sqlalchemy import select


def get_account(
    account_id: str = None,
    email_address: str = None,
    azure_ad_subject_id: str = None,
) -> Tuple[dict, int]:
    """
    Get a single account corresponding to the given unique parameters
    and return account object schema and status code
    :param account_id: (str) the id to search
    :param email_address: (str) the email to search
    :param azure_ad_subject_id: (str) the azure_ad_subject_id to search
    :return:
        Tuple of account object (or error) dict and status int
    """
    if not any([account_id, email_address, azure_ad_subject_id]):
        return {
            "error": (
                "Bad request: please provide at least 1 query argument of "
                "account_id, email_address or azure_ad_subject_id"
            )
        }, 400

    stmnt = select(Account)

    if account_id:
        stmnt = stmnt.filter(Account.id == account_id)
    if email_address:
        stmnt = stmnt.filter(Account.email == email_address)
    if azure_ad_subject_id:
        stmnt = stmnt.filter(Account.azure_ad_subject_id == azure_ad_subject_id)

    try:
        result = db.session.execute(stmnt)
        account = result.scalars().one()
        account_schema = AccountSchema()
        return account_schema.dump(account), 200
    except sqlalchemy.exc.NoResultFound:
        return {"error": "No matching account found"}, 404


def get_bulk_accounts(
    account_id: list,
) -> Dict:
    """
    Get multiple accounts corresponding to the given account ids
    and return account object schema and status code
    :param account_id: List of ids to search
    :return:
        Nested dict of account_id: {account object}
    """
    if not account_id:
        return {"error": "Bad request: please provide at least 1 account_id "}, 400

    stmnt = select(Account)
    stmnt = stmnt.filter(Account.id.in_(account_id))

    try:
        result = db.session.scalars(stmnt)
        account_schema = AccountSchema()

        accounts_metadatas = {
            str(account_row.id): account_schema.dump(account_row)
            for account_row in result
        }

        return accounts_metadatas, 200
    except sqlalchemy.exc.NoResultFound:
        return {"error": "No matching account found"}, 404


# old roles, we should remove these once all old roles are removed in azure
_DEPRECATED_ROLES = {"LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"}

_VALID_ROLES = {
    # legacy roles, always cof since they were original fund
    "ASSESSOR": "COF_ASSESSOR",
    "LEAD_ASSESSOR": "COF_LEAD_ASSESSOR",
    "COMMENTER": "COF_COMMENTER",
    # cof specific roles
    "COF_LEAD_ASSESSOR": "COF_LEAD_ASSESSOR",
    "COF_ASSESSOR": "COF_ASSESSOR",
    "COF_COMMENTER": "COF_COMMENTER",
    "COF_SCOTLAND": "COF_SCOTLAND",
    "COF_NORTHERNIRELAND": "COF_NORTHERNIRELAND",
    "COF_WALES": "COF_WALES",
    "COF_ENGLAND": "COF_ENGLAND",
    # nstf specific roles
    "NSTF_LEAD_ASSESSOR": "NSTF_LEAD_ASSESSOR",
    "NSTF_ASSESSOR": "NSTF_ASSESSOR",
    "NSTF_COMMENTER": "NSTF_COMMENTER",
}


def put_account(account_id: str) -> Tuple[dict, int]:
    """put_account Given an account id and a role,
    if the account_id exists in the db the corresponding
    entry in the db is updated with the corresponding role.

    Args:
        account_id (str, required): An account_id given as a string.
    Json Args:
        roles (str, required): An array of roles given as a string.
        azure_ad_subject_id (str, required): Subject id of the Azure AD object.
        email (str, optional): Preferred email of the account holder.
        full_name (str, optional): First and last name given as a string.
        Defaults to None.

    Returns:
        dict, int
    """
    # Validate request body
    try:
        roles = request.json["roles"]
    except KeyError:
        return {"error": "roles are required"}, 401
    try:
        azure_ad_subject_id = request.json["azure_ad_subject_id"]
    except KeyError:
        return {"error": "azure_ad_subject_id is required"}, 401

    full_name = request.json.get("full_name")
    email = request.json.get("email_address")

    # Check account exists
    try:
        account = (
            db.session.query(Account)
            .filter(
                Account.id == account_id,
                or_(
                    Account.azure_ad_subject_id == azure_ad_subject_id,
                    Account.azure_ad_subject_id.is_(None),
                ),
            )
            .one()
        )
    except sqlalchemy.exc.NoResultFound:
        return {"error": "No account matching those details could be found"}, 404
    # Check all roles are valid before doing any database updates
    for role in roles:
        try:
            _VALID_ROLES[role.upper()]
            if role.upper() in _DEPRECATED_ROLES:
                # TODO: Remove this once all legacy groups are removed/changed in Azure AD
                current_app.logger.warning(
                    f"Role '{role}' is deprecated, please use"
                    f" '{_VALID_ROLES[role.upper()]}' instead. This will need to be"
                    " changed in Azure AD."
                )
        except KeyError:
            return {"error": f"Role '{role}' is not valid"}, 401
    # Delete existing roles
    stmnt = delete(Role).where(Role.account_id == account_id)
    db.session.execute(stmnt)

    if email:
        try:
            account.email = email
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.flush()
            db.session.rollback()
            return {
                "error": (
                    f"Email '{email}' cannot be updated - "
                    "another account may already be using this email"
                )
            }, 401
    if full_name:
        account.full_name = full_name
    if azure_ad_subject_id:
        account.azure_ad_subject_id = azure_ad_subject_id

    # Update current roles
    current_roles = []
    for role in roles:
        current_role = Role()
        current_role.account_id = account_id
        current_role.role = _VALID_ROLES[role.upper()]
        current_roles.append(current_role)

    db.session.add_all(current_roles)

    db.session.commit()

    get_account_stmnt = select(Account).filter(Account.id == account_id)

    result = db.session.execute(get_account_stmnt)
    account = result.scalars().one()
    account_schema = AccountSchema()

    return account_schema.dump(account), 201


def post_account() -> Tuple[dict, int]:
    """
    Creates a new account in the db, given an email (required)
    and optional azure_ad_subject_id.

    If an account with this email address already exists then a 409
    is returned, otherwise a 201 is returned.

    Json Args:
        email_address (str, required): An valid email given as a string.
        azure_ad_subject_id (str, optional):
            An Azure AD subject ID given as a string.

    Returns:
        Returns a dictionary(json) along with a status code.
    """
    email_address = request.json.get("email_address")
    azure_ad_subject_id = request.json.get("azure_ad_subject_id")
    if not email_address:
        return {"error": "email_address is required"}, 400
    try:
        new_account = Account(
            email=email_address, azure_ad_subject_id=azure_ad_subject_id
        )
        db.session.add(new_account)
        db.session.commit()
        new_account_json = {
            "account_id": new_account.id,
            "email_address": email_address,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        return new_account_json, 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return (
            "An account with that email or azure_ad_subject_id already exists",
            409,
        )
