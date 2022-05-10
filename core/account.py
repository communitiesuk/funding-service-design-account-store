"""
Contains the functions directly used by the openapi spec.
"""
from typing import Tuple

import shortuuid
from core.data_operations.account_data import check_exists_then_get
from core.data_operations.account_data import get_data_by_email
from core.db.db_connection import db_connection


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

    if email_address is None and account_id is None:
        return "", 404

    if (email_address and account_id) or account_id:
        return check_exists_then_get(account_id)

    if email_address and account_id is None:
        return get_data_by_email(email_address)


def post_account_by_email(email_address: str) -> Tuple[dict, int]:
    """post_account_by_email Given an email address creates a new account in the
    db.

    If an account with this email address already exists then a 409
     is returned,
    otherwise a 200 is returned.

    Args:
        email_address (str): An valid email given as a string.

    Returns:
        Returns a dictionary(json) along with a status code.
    """

    if db_connection.exists(f"email_{email_address}"):
        return "An account with that email already exists", 409

    else:
        new_account_id = shortuuid.uuid()
        db_connection.set(f"email_{email_address}", new_account_id)
        new_account_json = {
            "account_id": new_account_id,
            "email_address": email_address,
            "applications": [],
        }
        db_connection.set(new_account_id, new_account_json)

        return new_account_json
