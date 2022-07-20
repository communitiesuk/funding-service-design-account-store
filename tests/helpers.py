from typing import Tuple


def get_and_return_data(client, email_address=None, account_id=None):

    if email_address is None and account_id is None:
        raise TypeError("Atleast 1 argument must be given.")

    if email_address is not None and account_id is not None:
        raise TypeError("Only one kwarg can be given.")

    raw_params = {"email_address": email_address, "account_id": account_id}

    params = {k: v for k, v in raw_params.items() if v is not None}
    url = "/accounts"

    response = client.get(url, query_string=params)

    print(response)

    return response


def post_email_and_return_data(client, email_address: str) -> Tuple[int, dict]:

    params = {"email_address": email_address}
    url = "/accounts"

    response = client.post(url, json=params)

    return response.status_code, response.json
