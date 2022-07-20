"""
Contains the functions directly used by the openapi spec.
"""
from typing import Tuple

import sqlalchemy
from core.data_operations.account_data import check_exists_then_get
from core.data_operations.account_data import get_data_by_email
from db import db
from db.models.account import Account
from flask import request


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
        return check_exists_then_get(account_id)
    elif email_address:
        return get_data_by_email(email_address)
    else:
        raise TypeError("Get account needs atleast 1 argument.")


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
                    "email_address": email_address,
                    "applications": [],
                }
                return new_account_json, 201
            except sqlalchemy.IntegrityError:
                db.rollback()
        else:
            return "An account with that email already exists", 409


# def post_application_to_account():

#     application_id = request.json.get("application_id")
#     account_id = request.json.get("account_id")

#     pass
