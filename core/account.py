import shortuuid
from core.data_operations.account_data import check_exists_then_get
from core.data_operations.account_data import get_data_by_email
from core.db.db_connection import db_connection


def get_account(email_address=None, account_id=None):

    if email_address is None and account_id is None:

        return "", 404

    if (email_address and account_id) or account_id:

        return check_exists_then_get(account_id)

    if email_address and not account_id:

        return get_data_by_email(email_address)


def post_account_by_email(email_address):

    if db_connection.exists(f"email_{email_address}"):

        return 409

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
