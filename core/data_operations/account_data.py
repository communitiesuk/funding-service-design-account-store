from typing import Tuple

import sqlalchemy
from connexion import NoContent
from db import db
from db.models.account import Account


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
            }
        else:
            return account
    except sqlalchemy.exc.NoResultFound:
        return NoContent, 404


def get_account_data_by_email(email: str, as_json: bool = True) -> Tuple[dict, int]:
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
