import os
import requests

from requests.auth import HTTPBasicAuth

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

JIRA_URL = os.environ["JIRA_URL"]
JIRA_AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


def _jira_request(url, **kwargs):
    return requests.request(
        auth=JIRA_AUTH,
        url=JIRA_URL + url,
        **kwargs
    )


def get(url, **kwargs):
    return _jira_request(url, method="GET", **kwargs)


def post(url, **kwargs):
    return _jira_request(url, method="POST", **kwargs)


def put(url, **kwargs):
    return _jira_request(url, method="PUT", **kwargs)


def delete(url, **kwargs):
    return _jira_request(url, method="DELETE", **kwargs)
