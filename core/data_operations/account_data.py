from typing import Tuple

import sqlalchemy
from connexion import NoContent
from db import db
from db.models import account


def check_exists_then_get(account_id: str) -> Tuple[dict, int]:
    """check_exists_then_get Checks that the key exists in the db
     and returns a value if so.

    Args:
        key (str): A key we would like the query in our db.

    Returns:
        A tuple with content and a status code.
    """

    try:
        db.session.query(account).filter(account.id == account_id).one()
    except sqlalchemy.exc.NoResultFound:
        return NoContent, 404


def get_data_by_email(email: str) -> Tuple[dict, int]:
    """get_data_by_email Allows you to fetch account by its email.

    Args:
        email (str): An email given a str.

    Returns:
        A tuple with content and a status code.
    """

    try:
        db.session.query(account).filter(account.email == email).one()
    except sqlalchemy.exc.NoResultFound:
        return NoContent, 404
