import json
import subprocess
import jira_requests

TRANSITION_ID = "51"  # Ready for Test


def prompt_yn(email, issue_count):
    response = input(f"Moving {issue_count} issues for {email}.: [y/n]").lower()
    if response[0].lower() != "y":
        print("You exited")
        exit(1)


def git_email():
    return subprocess.check_output(
        ["git", "config", "user.email"], encoding="UTF-8"
    ).split("@")[0]


def search_issues(jql):
    return jira_requests.get(
        "/rest/api/2/search",
        params={"jql": jql},
    ).json()["issues"]


def set_issues(issue_ids_or_keys):
    for issue_id_or_key in issue_ids_or_keys:
        response = jira_requests.post(
            f"/rest/api/2/issue/{issue_id_or_key}/transitions",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"transition": {"id": TRANSITION_ID}}),
        )

        print(f"issue: {issue_id_or_key}", response)


GIT_EMAIL = git_email()
ISSUES = search_issues(f'assignee = {GIT_EMAIL} AND status = "Ready for Stage"')

ISSUE_COUNT = len(ISSUES)
ISSUE_KEYS = [issue["key"] for issue in ISSUES]

prompt_yn(GIT_EMAIL, ISSUE_COUNT)
set_issues(ISSUE_KEYS)
