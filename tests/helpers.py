import ast
from typing import Tuple

from flask import request
from requests import PreparedRequest


def get_and_return_data(client, email_address=None, account_id=None):

    if email_address is None and account_id is None:
        raise TypeError("Atleast 1 argument must be given.")

    if email_address is not None and account_id is not None:
        raise TypeError("Only one kwarg can be given.")

    raw_params = {"email_address": email_address, "account_id": account_id}

    params = {k: v for k, v in raw_params.items() if v is not None}
    req = PreparedRequest()
    root_url = request.root_url
    url = root_url + "account"
    req.prepare_url(url, params)

    response = client.get(req.url)

    return response


def post_email_and_return_data(client, email_address: str) -> Tuple[int, dict]:

    params = {"email_address": email_address}
    req = PreparedRequest()
    root_url = request.root_url
    url = root_url + "account"
    req.prepare_url(url, params)

    response = client.post(req.url)
    post_response_data = response.data

    # turns the bytestring into a python dictionary.
    response_dict = ast.literal_eval(post_response_data.decode("utf-8"))

    return response.status_code, response_dict
