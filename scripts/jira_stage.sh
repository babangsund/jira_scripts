#!/bin/bash

sha=$1
message=$2
issue=$(echo $message | grep -o 'DEV-[0-9][0-9]*')

echo "Attempting to move JIRA issue $issue."

if [[ ! $issue ]]; then
  echo "Issue: '$issue' is not a valid JIRA issue."
  exit 0
fi

jira_url=JIRA_BASE_URL
jira_auth="JIRA_USER:JIRA_PASSWORD"

# Transitions the JIRA issue to Ready for Stage
# 101 = Ready for Stage
transition() {
  curl --request POST \
    --user $jira_auth \
    --url $jira_url/rest/api/2/issue/$issue/transitions \
    --header "Content-Type: application/json" \
    --data '{"transition":{"id":101}}'
}

# Adds a fixVersion to the JIRA issue
version() {
  v=JIRA_RELEASE_VERSION
  curl --request POST \
    --user $jira_auth \
    --url $jira_url/rest/api/2/issue/$issue \
    --header "Content-Type: application/json" \
    --data "{
      \"update\": { \"fixVersions\": [{\"add\": \"$v\"}] }
    }"
}

# Adds a comment to the JIRA issue
# Listing the commits that were merged
comment() {
  url=$jira_url/rest/api/2/issue/$issue/comment
  commits=$(git rev-list --abbrev-commit --no-merges --reverse $sha^..$sha)
  body=$(echo $commits | sed 's/ /\\n/g')
  curl --request POST \
    --user $jira_auth \
    --url $jira_url/rest/api/2/issue/$issue/comment \
    --header "Content-Type: application/json" \
    --data "{
      \"body\": \"Merged commits:\n\n$body\"
    }"
}


transition
comment
version
