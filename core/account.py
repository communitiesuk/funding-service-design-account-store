import shortuuid
from connexion import NoContent
from core.dumb_data_store import dummmy_db_connection

if True:

    db_connection = dummmy_db_connection()

else:

    db_connection = "a real connection"


def get_account_by_email(email_address=None, account_id=None):

    if email_address is None and account_id is None:

        return 404

    if email_address and account_id:

        if not db_connection.exists(account_id):

            return NoContent, 204

        return db_connection.get(account_id)

    if email_address:

        if not db_connection.exists(f"email_{email_address}"):

            return NoContent, 204

        account_id = db_connection.get(f"email_{email_address}")

        return db_connection.get(account_id)

    if account_id:

        if not db_connection.exists(account_id):

            return NoContent, 204

        return db_connection.get(account_id)


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
