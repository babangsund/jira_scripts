import os
import json
import subprocess

import requests
from requests.auth import HTTPBasicAuth

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

TRANSITION_ID = "51"  # Ready for Test
JIRA_URL = os.environ["JIRA_URL"]
JIRA_AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


def prompt_yn(email, issue_count):
    response = input(f"Moving {issue_count} issues for {email}.: [y/n]").lower()
    if response[0].lower() != "y":
        print("You exited")
        exit(1)


def get_name():
    return subprocess.check_output(
        ["git", "config", "user.email"], encoding="UTF-8"
    ).split("@")[0]


def get_issues(git_email):
    return requests.get(
        JIRA_URL + "/rest/api/2/search",
        auth=JIRA_AUTH,
        params={"jql": f'assignee = {git_email} AND status = "Ready for Stage"'},
    ).json()["issues"]


def set_issues(issue_ids_or_keys):
    for issue_id_or_key in issue_ids_or_keys:
        response = requests.post(
            JIRA_URL + f"/rest/api/2/issue/{issue_id_or_key}/transitions",
            auth=JIRA_AUTH,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"transition": {"id": TRANSITION_ID}}),
        )

        print(f"issue: {issue_id_or_key}", response)


GIT_EMAIL = get_name()
ISSUES = get_issues(GIT_EMAIL)

ISSUE_COUNT = len(ISSUES)
ISSUE_KEYS = [issue["key"] for issue in ISSUES]

prompt_yn(GIT_EMAIL, ISSUE_COUNT)
set_issues(ISSUE_KEYS)
