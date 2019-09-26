# Various scripts for interacting with JIRA from the terminal.

`jira_requests.py`: get, post, put, delete with pre-applied auth and base url.  
`jira_version.py`: Version class, fetching or creating most recent JIRA version.  
`jira_ready_for_test.py`: Moves all your issues from `Ready for Stage` to `Ready for Test`.  
`jira_mr.sh` Rebase, merge, push and transition an issue to `Ready for Stage`.  
`jira_stage.sh` Transitions the issue to `Ready for Stage`, and adds a comment with all the merged commits.
