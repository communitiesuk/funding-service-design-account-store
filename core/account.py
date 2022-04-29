from core.dumb_data_store import dummmy_db_connection

if True:

    db_connection = dummmy_db_connection()

else:

    db_connection = "a real connection"


def get_account_by_email(email_address=None, account_id=None):

    if email_address is None and account_id is None:

        return 404

    if email_address and account_id:

        print("both given")

        return 200

    if email_address:

        print("email given")

        return 200

    if account_id:

        print("account id given")

        return 200


def post_account_by_email():

    print("post account worked")
