
from tldt.tldt import Project
import ConfigParser
import argparse
import json
import os.path
import requests
import time


class Poller():
    
    def __init__(self, config):
        self.config = config
        self.username = self.config.get("Auth", "username")
        self.password = self.config.get("Auth", "password")
        self.git_user = self.config.get("Auth", "repo_owner")
        self.repo = self.config.get("Auth", "repo_name")
        self.poll_interval = self.config.get("Poller", "poll_interval")

    def get_content_from_url(self, url):
        r = requests.get(url)
        if (r.ok):
            content = json.loads(r.content)
            return content
        else:
            raise Exception ("Pull request list not accessible. Verify if the git_user and repo are correct.")
    
    def extract_substring_between_borders(self, big_string, left_border, right_border):
        return big_string[big_string.index(left_border) + len(left_border) : big_string.index(right_border)]
    
    
    
    def get_all_open_pull_requests(self):
        all_pulls_list_url = self.get_content_from_url("https://api.github.com/repos/%s/%s/pulls" % (self.git_user, self.repo))
        return all_pulls_list_url
        
    def get_latest_open_pull_request(self):
        return self.get_all_open_pull_requests()[0]
    
    def get_pull_request_number(self, pull_request):
        return pull_request['number']
    
    def get_head_sha_for_pull_request(self, pull_request):
        return pull_request['head']['sha']
    
    def get_head_repo_fullname_for_pull_request(self, pull_request):
        return pull_request['head']['repo']['full_name']
    
    def get_base_sha_for_pull_request(self, pull_request):
        return pull_request['base']['sha']
    
    def get_base_repo_fullname_for_pull_request(self, pull_request):
        return pull_request['base']['repo']['full_name']
    
    def get_comments_for_pull_request(self, pull_request):
        pull_req_number = self.get_pull_request_number(pull_request)
        all_comments = self.get_content_from_url("https://api.github.com/repos/%s/%s/issues/%d/comments" % (self.git_user, self.repo, pull_req_number) )
        return all_comments
    
    def get_latest_comment_by_user(self, comments_list, user):
        index = len(comments_list)-1
        while index >= 0:
            if comments_list[index]['user']['login'] == user:
                return comments_list[index]['body']
            index -= 1
        return None
    
    def extract_sha_from_comment(self, comment):
        return self.extract_substring_between_borders(comment, "revised for sha ", ".")
    
    def run_tldt_for_pull_request_if_needed(self, pull_request):
        comments_list = self.get_comments_for_pull_request(pull_request)
        latest_comment_by_tldl = self.get_latest_comment_by_user(comments_list, "tldl")
        if latest_comment_by_tldl == None: # new pull request
            Project(self.get_head_sha_for_pull_request(pull_request), 
                    self.get_head_repo_fullname_for_pull_request(pull_request), 
                    self.get_base_repo_fullname_for_pull_request(pull_request), 
                    self.get_base_sha_for_pull_request(pull_request), 
                    config=self.config).tldt()
        else:
            revised_sha = self.extract_sha_from_comment(latest_comment_by_tldl)
            if revised_sha !=  self.get_head_sha_for_pull_request(pull_request): # commits exist after previous test run
                Project(self.get_head_sha_for_pull_request(pull_request), 
                    self.get_head_repo_fullname_for_pull_request(pull_request), 
                    self.get_base_repo_fullname_for_pull_request(pull_request), 
                    self.get_base_sha_for_pull_request(pull_request), 
                    config=self.config).tldt()
    
    def parse_all_open_pull_requests(self):
        for pull_request in self.get_all_open_pull_requests():            
            self.run_tldt_for_pull_request_if_needed(pull_request)

    def poll(self):
        while True:
            self.parse_all_open_pull_requests()
            time.sleep(int(float(self.poll_interval)))
    
    

def main():
    user_home = os.path.expanduser("~")
    parser = argparse.ArgumentParser(description="xx")
    parser.add_argument("--configuration", default=os.path.join(user_home, "tldt.ini"))
    args = parser.parse_args()
    config = ConfigParser.ConfigParser(args.configuration)
    poller = Poller(config)
    poller.poll()
    
if __name__ == "__main__":
    main()


'''
ALGORITHM: 
     - New PR: no comment by tldl
         - run tests
         - comment made by tldt: "revised for sha {sha}"
     - Already Revised PR: if (comment made by tldt: "revised for sha {sha}" & {sha}!=head_sha)
         - run tests
         - comment made by tldt: "revised for sha {sha}"
'''