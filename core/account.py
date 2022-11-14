"""
Contains the functions directly used by the openapi spec.
"""
from typing import Tuple

import sqlalchemy
from core.data_operations.account_data import check_account_exists_then_return
from core.data_operations.account_data import get_account_data_by_email
from core.data_operations.account_data import update_account
from db import db
from db.models.account import Account
from db.models.account import Role
from flask import request
from flask import current_app
from config import Config
import json


def get_account(
    email_address: str = None, account_id: str = None
) -> Tuple[dict, int]:
    """get_account Given an email or account id, the corresponding
    entry in the db is returned.

    Args:
        email_address (str, optional): An email address given as a string.
        Defaults to None.
        account_id (_type_, optional): An account_id given as a string.
        Defaults to None.

    Returns:
        dict, int
    """

    if account_id:
        return check_account_exists_then_return(account_id)
    elif email_address:
        return get_account_data_by_email(email_address)
    else:
        raise TypeError("GET account needs at least 1 argument.")


def put_account(
    account_id: str
) -> Tuple[dict, int]:
    """put_account Given an account id and an optional role,
    if the account_id exists in the db the corresponding
    entry in the db is updated with the corresponding role.

    Args:
        account_id (str, required): An account_id given as a string.
    Json Args:
        role (str, required): A role given as a string.
        Defaults to None.

    Returns:
        dict, int
    """
    role = request.json.get("role")
    if not role:
        return {"error": "role is required"}, 401
    else:
        account = update_account(account_id, role)
        return account


def put_updates_to_account_roles() -> Tuple[dict, int]:
    """
    Bulk update account roles using either

    Given a request json object with a structure of
         {
             roles: { email: role,... }
        }
    then for each email key in the roles object:
        if the email exists in the db
        then update the corresponding entry in the db with the corresponding role.

    Returns:
        dict, int
    """
    roles = request.json.get("roles")
    if not roles:
        return {"error": "incorrectly formatted payload"}, 401

    return update_account_roles(roles)


def update_account_roles(roles: dict) -> Tuple[dict, int]:
    """
    Bulk update account roles using either

    Args:
        roles (dict): { email: role,...}

    For each email key in roles:
        if the email exists in the db
        then the corresponding entry in the db is updated with the corresponding role.

    Returns:
        dict, int
    """

    # First CHECK all accounts exist and roles are valid before updating anything
    valid_accounts = {}
    for email, role in roles.items():
        account, code = get_account(email_address=email)
        masked_email = email[0:4] + "****" + email[-6:]
        if code != 200:
            current_app.logger.error(f"Account with email {masked_email} does not exist")
            return {"error": f"Account with email {masked_email} does not exist"}, 401
        try:
            Role[role]
        except KeyError:
            current_app.logger.error(
                f"Tried to set non-existent role "
                f"'{role}' for account with email {masked_email}"
            )
            return {
                       "error": f"Tried to set non-existent role "
                                f"'{role}' for account with email {masked_email}"
                   }, 401
        valid_accounts.update({
            account["account_id"]: role
        })

    # Then UPDATE all account roles if all valid
    for account_id, role in valid_accounts.items():
        updated_account, update_status = update_account(account_id, role)
        if not update_status == 201:
            current_app.logger.error(
                f"Account with id {account_id} could not be updated"
            )
            return {"error": f"Account with id {account_id} could not be updated"}, 401
    current_app.logger.info("Account roles updated")

    # Finally, RETURN updated roles as confirmation
    return roles, 201


def post_account_by_email() -> Tuple[dict, int]:
    """post_account_by_email Given an email address creates a new account in the
    db.

    If an account with this email address already exists then a 409
     is returned,
    otherwise a 201 is returned.

    Json Args:
        email_address (str): An valid email given as a string.

    Returns:
        Returns a dictionary(json) along with a status code.
    """
    email_address = request.json.get("email_address")
    if not email_address:
        return {"error": "email_address is required"}, 400
    else:
        email_exists = bool(
            db.session.query(Account)
            .filter(Account.email == email_address)
            .first()
        )
        if not email_exists:
            try:
                new_account = Account(email=email_address)
                db.session.add(new_account)
                db.session.commit()
                new_account_json = {
                    "account_id": new_account.id,
                    "role": new_account.role.name,
                    "email_address": email_address,
                    "applications": [],
                }
                return new_account_json, 201
            except sqlalchemy.IntegrityError:
                db.rollback()
                return "Integrity Error", 500
        else:
            return "An account with that email already exists", 409
