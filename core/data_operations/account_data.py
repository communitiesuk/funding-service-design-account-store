from typing import Tuple

from connexion import NoContent
from core.db.db_connection import db_connection


def check_exists_then_get(key: str) -> Tuple[dict, int]:
    """check_exists_then_get Checks that the key exists in the db
     and returns a value if so.

    Args:
        key (str): A key we would like the query in our db.

    Returns:
        A tuple with content and a status code.
    """

    try:
        return db_connection.get(key)
    except KeyError:
        return NoContent, 404


def get_data_by_email(email: str) -> Tuple[dict, int]:
    """get_data_by_email Allows you to fetch account by its email.

    Args:
        email (str): An email given a str.

    Returns:
        A tuple with content and a status code.
    """

    address_id = check_exists_then_get(f"email_{email}")

    return check_exists_then_get(address_id)
