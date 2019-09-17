import os
import json
import re
import subprocess
import jira_requests

from dateutil.parser import parse

PROJECT_ID = os.environ["PROJECT_ID"]


def _git_version_info():
    describe_output = subprocess.check_output(
        ["git", "describe", "--long"], encoding="UTF-8"
    )

    [version_number, since_number] = describe_output.split("-")
    since_number = int(since_number)

    if since_number == 0:
        # This is a release version
        is_release = 1
        describe_output = subprocess.check_output(
            ["git", "describe", "--long", "HEAD~1"], encoding="UTF-8"
        )

    else:
        # This is NOT a release version
        is_release = 0
        version_number = version_number + "-beta-" + str(since_number)

    [previous_version_number, since_number] = describe_output.split("-")
    since_number = int(since_number)

    return (is_release, since_number, version_number, previous_version_number)


def _get_version(version_number):
    """Loop over versions for project - not possible to search them in api"""
    """Testing if provided version_number is a JIRA version"""

    version_id = None
    version_name = None

    response = jira_requests.get(
        f"/rest/api/2/project/{PROJECT_ID}/version/?orderBy=-releaseDate&maxResults=50"
    ).json()

    for attrs in response["values"]:
        if attrs["name"] == version_number:
            version_id = attrs["id"]
            version_name = attrs["name"]
            break

    return (version_id, version_name)


def _new_version(is_release, version_number):
    """Get date + author from tag (could be different from commit)"""

    if is_release == 1:
        show_output = subprocess.check_output(
            ["git", "show", version_number], encoding="UTF-8"
        )
        m = re.search(r"Tagger: (.+)", show_output, re.M)
        tag_author = m.group(1)
        m = re.search(r"Date: (.+)", show_output, re.M)
        tag_date = parse(m.group(1)).date()
    else:
        show_output = subprocess.check_output(["git", "show"], encoding="UTF-8")
        m = re.search(r"Author: (.+)", show_output, re.M)
        tag_author = m.group(1)
        m = re.search(r"Date: (.+)", show_output, re.M)
        tag_date = parse(m.group(1)).date()

    payload = {
        "released": "true",
        "overdue": "false",
        "archived": "false",
        "name": version_number,
        "projectId": PROJECT_ID,
        "releaseDate": str(tag_date),
        "description": "Version " + version_number + " by " + tag_author,
    }

    response = jira_requests.post("/rest/api/2/version", json=payload)
    if response.status_code >= 400:
        print("Error creating version: " + str(response.status_code))

    r = json.loads(response.text)
    version_id = r["id"]
    version_name = r["name"]

    return (version_id, version_name)


class Version:
    def __init__(self):
        (
            is_release,
            since_number,
            version_number,
            previous_version_number,
        ) = _git_version_info()

        (version_id, version_name) = _get_version(version_number)

        if not version_id or not version_name:
            (version_id, version_name) = _new_version(is_release, version_number)

        self.id = version_id
        self.name = version_name
        self.number = version_number
        self.is_release = is_release
        self.since_number = since_number
        self.previous_number = previous_version_number

        print(self.__repr__())

    def __repr__(self):
        return f"Version: {self.name} - {self.id}"
