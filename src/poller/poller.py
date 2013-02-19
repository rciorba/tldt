import json
import requests


git_user = "django"
repo = "django"

def get_all_open_pull_requests():
    all_pulls_list_url = "https://api.github.com/repos/%s/%s/pulls" % (git_user, repo)
    r = requests.get(all_pulls_list_url)
    if (r.ok):
        all_pull_requests = json.loads(r.content)
        return all_pull_requests
    else:
        raise Exception ("Pull request list not accessible. Verify if the git_user and repo are correct.")

def get_latest_open_pull_request():
    return get_all_open_pull_requests()[0]

def get_pull_request_number(pull_request):
    return pull_request['number']

def get_head_sha_for_pull_request(pull_request):
    return pull_request['head']['sha']

def get_head_repo_fullname_for_pull_request(pull_request):
    return pull_request['head']['repo']['full_name']

def get_base_sha_for_pull_request(pull_request):
    return pull_request['base']['sha']

def get_base_repo_fullname_for_pull_request(pull_request):
    return pull_request['base']['repo']['full_name']

def get_comments_for_pull_request(pull_request):
    pull_req_number = get_pull_request_number(pull_request)
    all_comments_url = "https://api.github.com/repos/%s/%s/issues/%d/comments" % (git_user, repo, pull_req_number)
    r = requests.get(all_comments_url)
    if (r.ok):
        all_comments = json.loads(r.content)
        return all_comments
    else:
        raise Exception ("Pull request list not accessible. Verify if the git_user and repo are correct.")

def get_timestamp_for_latest_comment_by_user(comments_list, user):
    index = len(comments_list)-1
    while index >= 0:
        if comments_list[index]['user']['login'] == user:
            return comments_list[index]['updated_at']
        index -= 1
    return None





file_readed = open("comments.json")
all_comments = json.loads(file_readed.read())

print get_timestamp_for_latest_comment_by_user(all_comments, "mzetea")


'''
TO DO: 
- parse string to timestamp

- implement algorithm for running tests on:
     - New PR
         - run tests
         - comment made by tldt: revised
     - Revised PR
         - if (post_commits_exist)
             - run tests
             - comment made by tldt: revised
'''