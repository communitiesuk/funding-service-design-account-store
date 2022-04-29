from connexion import NoContent
from core.db.db_connection import db_connection


def check_exists_then_get(key):

    if not db_connection.exists(key):

        return NoContent, 204

    return db_connection.get(key)


def get_data_by_email(email):

    address_id = check_exists_then_get(f"email_{email}")

    return check_exists_then_get(address_id)
