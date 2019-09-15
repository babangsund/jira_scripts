import os
import requests

from requests.auth import HTTPBasicAuth

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

JIRA_URL = os.environ["JIRA_URL"]
JIRA_AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


def __jira_request__(url, **kwargs):
    return requests.request(
        auth=JIRA_AUTH,
        url=JIRA_URL + url,
        **kwargs
    )


def get(url, **kwargs):
    return __jira_request__(url, method="GET", **kwargs)


def post(url, **kwargs):
    return __jira_request__(url, method="POST", **kwargs)


def put(url, **kwargs):
    return __jira_request__(url, method="PUT", **kwargs)


def delete(url, **kwargs):
    return __jira_request__(url, method="DELETE", **kwargs)
