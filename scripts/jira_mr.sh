#!/bin/bash
set -e

branch=$1
jira_user=$2
jira_base_url=$3

n=$'\n'
jira_issue=$(echo $1 | sed 's/.*\///g')

exit_prompt() {
  msg=$1
  read -p "$msg [y/n] $n" -n 1 -r
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
  fi
  echo $n
}

gco_branch() {
  if [[ ! `git rev-parse --abbrev-ref HEAD` == "master" ]]; then
    git checkout $1
  fi
}

branch_exist=`git show-ref refs/heads/${branch}`
if [[ ! $branch_exist ]]
then
    echo ERROR: The branch $branch does not exist.
    exit 1
fi

exit_prompt "Are you sure you want to merge $branch into master?"
gco_branch "master"

echo "${n}Pulling the latest changes from origin/master$n"
git pull

rebase_required=$(git rev-list $branch..master)
if [[ ! -z $rebase_required ]]
then
  echo "The branch $branch requires a rebase before it can be merged."
  exit_prompt "Rebase $branch on top of master?"

  git rebase master $branch > /dev/null 2>&1
  if [[ ! $? -eq 0 ]];
  then
      echo "Encountered a conflict while rebasing.$n"
      git rebase --abort
      exit 1
  fi
  echo "Rebased successfully.$n"
  gco_branch "master"
fi

echo $n$n

exit_prompt "Merge $branch into master, and pushing to origin. Continue?"
git merge --no-ff $branch

git push \
  && git branch -d $branch \
  && git push origin --delete $branch

echo $n$n

exit_prompt "Transition JIRA issue $jira_issue to Ready for Stage?"
curl -u $jira_user \
     -H "Content-Type: application/json" \
     -d '{"transition":{"id":101}}' \
     -XPOST $jira_base_url/rest/api/2/issue/$jira_issue/transitions
