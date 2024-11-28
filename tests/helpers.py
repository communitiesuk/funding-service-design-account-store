import re
from json import loads
from typing import List

from deepdiff import DeepDiff


def expected_data_within_response(
    test_client,
    endpoint: str,
    expected_data,
    expected_status_code: int,
    method="get",
    data=None,
    json=None,
    exclude_regex_paths=None,
    **kwargs,
):
    """
    Given an endpoint and expected content,
    check to see if response contains expected data

    Args:
        test_client: A flask test client
        endpoint (str): The request endpoint
        method (str): The method of the request
        data: The data to post/put if required
        json: The json to post/put if required
        expected_data: The content we expect to find
        expected_status_code (int): The status code we expect
        exclude_regex_paths: paths to exclude from diff

    """
    if method == "put":
        response = test_client.put(
            endpoint, data=data, json=json, follow_redirects=True
        )
    elif method == "post":
        response = test_client.post(
            endpoint, data=data, json=json, follow_redirects=True
        )
    else:
        response = test_client.get(endpoint, follow_redirects=True)

    assert (
        response.status_code == expected_status_code
    ), f"Expected {str(expected_status_code)} response status code but got {str(response.status_code)}"
    response_data = loads(response.content)
    diff = DeepDiff(
        expected_data,
        response_data,
        exclude_regex_paths=exclude_regex_paths,
        **kwargs,
    )
    error_message = "Expected data does not match response: " + str(diff)
    assert diff == {}, error_message


def key_list_to_regex(exclude_keys: List[str] = []):
    """
    Helper function to go with DeepDiff expected_data_within_response()
    Converts a list of dictionary keys eg. ['account_id','timestamp']
        into a list of re.compile objects to pass to the
        exclude_regex_paths parameter of DeepDiff(exclude_regex_paths=...).
        This enables DeepDiff to ignore matching for the given keys
        for example if the key cannot be known in advance
        (eg. a dynamically generated UUID or timestamp)
    :param exclude_keys: a list of dictionary keys eg. ['account_id']
    :return:
    """
    exclude_regex_path_strings = [rf"root\['{key}'\]" for key in exclude_keys]
    regex_paths = exclude_regex_path_strings
    return [re.compile(regex_string) for regex_string in regex_paths]
