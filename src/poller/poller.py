import json
import requests


git_user = "django"
repo = "django"

def get_content_from_url(url):
    r = requests.get(url)
    if (r.ok):
        content = json.loads(r.content)
        return content
    else:
        raise Exception ("Pull request list not accessible. Verify if the git_user and repo are correct.")

def extract_substring_between_borders(big_string, left_border, right_border):
    return big_string[big_string.index(left_border) + len(left_border) : big_string.index(right_border)]



def get_all_open_pull_requests():
    all_pulls_list_url = get_content_from_url("https://api.github.com/repos/%s/%s/pulls" % (git_user, repo))
    return all_pulls_list_url
    
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
    all_comments = get_content_from_url("https://api.github.com/repos/%s/%s/issues/%d/comments" % (git_user, repo, pull_req_number) )
    return all_comments

def get_latest_comment_by_user(comments_list, user):
    index = len(comments_list)-1
    while index >= 0:
        if comments_list[index]['user']['login'] == user:
            return comments_list[index]['body']
        index -= 1
    return None

#def get_author_for_pull_request(pull_request):
#    return pull_request['user']['login']
#
#def get_commits_for_pull_request(pull_request):
#    pull_req_number = get_pull_request_number(pull_request)
#    all_commits = get_content_from_url("https://api.github.com/repos/%s/%s/pulls/%d/commits" % (git_user, repo, pull_req_number) )
#    return all_commits

def extract_sha_from_comment(comment):
    return extract_substring_between_borders(comment, "revised for sha ", ".")


file_readed = open("comments.json")
all_comments = json.loads(file_readed.read())


def run_tests_for_pull_request_if_needed(pull_request):
    comments_list = get_comments_for_pull_request(pull_request)
    latest_comment_by_tldl = get_latest_comment_by_user(comments_list, "tldl")
    if latest_comment_by_tldl == None: # new pull request
        print "new run"
        run_tests()
    else:
        revised_sha = extract_sha_from_comment(latest_comment_by_tldl)
        if revised_sha !=  get_head_sha_for_pull_request(pull_request): # commits exist after previous test run
            print "run again"
            run_tests()
            
def run_tests():
    print "tests ran"

run_tests_for_pull_request_if_needed(get_latest_open_pull_request())


'''
ALGORITHM: 
     - New PR: no comment by tldl
         - run tests
         - comment made by tldt: "revised for sha {sha}"
     - Already Revised PR: if (comment made by tldt: "revised for sha {sha}" & {sha}!=head_sha)
         - run tests
         - comment made by tldt: "revised for sha {sha}"
'''