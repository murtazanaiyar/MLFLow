"""
A python script to list changed files in a specified pull request.

Usage:
---------------------------------------------------------------------------
# List changed files in https://github.com/mlflow/mlflow/pull/3191
$ python dev/list_changed_files.py --repository mlflow/mlflow --pr-num 3191
---------------------------------------------------------------------------
"""
import argparse
import os
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", help="Owner and repository name", required=True)
    parser.add_argument("--pr-num", help="Pull request number", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    changed_files = []
    per_page = 100
    page = 1
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else None
    # Ref: https://docs.github.com/en/rest/reference/pulls#list-pull-requests-files
    url = f"https://api.github.com/repos/{args.repository}/pulls/{args.pr_num}/files"
    while True:
        resp = requests.get(url, params={"per_page": per_page, "page": page}, headers=headers)
        resp.raise_for_status()
        files = resp.json()
        changed_files.extend(f["filename"] for f in files)
        if len(files) < per_page:
            break
        page += 1

    print("\n".join(changed_files))


if __name__ == "__main__":
    main()
