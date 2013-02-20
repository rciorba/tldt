from __future__ import absolute_import
import contextlib
import ConfigParser
import importlib
import os
import subprocess

from tldt import git


@contextlib.contextmanager
def chdir(dirname):
    cwd = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(cwd)


class Project(object):

    def __init__(self, head_repo, head_sha, base_repo, base_sha,
                 configuration_path):
        self.head_repo = head_repo
        self.head_sha = head_sha
        self.base_repo = base_repo
        self.base_sha = base_sha
        self.config = ConfigParser.ConfigParser()
        self.config.read(configuration_path)
        self.parsers = self.config.items("ActiveParsers")
        self.repo = None
        # FOOBAR
        self.tldt()

    def checkout_code(self):
        self.repo = git.Repo(self.config.get("repo", "local"))
        self.repo.clone_or_update(self.base_repo)
        self.repo.fetch(self.head_repo)
        self.repo.checkout(self.head_sha)

    def setup_environment(self):
        with chdir(self.repo.local):
            subprocess.check_call(["build/setup_environment"])

    def run_tests(self):
        with chdir(self.repo.local):
            subprocess.check_call(["build/run_tests"])

    def run_parsers(self):
        for parser_name, parser_module in self.parsers:
            try:
                module = importlib.import_module(parser_module)
                kargs = dict(self.config.items("parser-%s" % parser_name))
                module.Parser(**kargs)
            except ImportError as e:
                print "Could not load '%s' parsing module.Skipping...\n %r " % (parser_name, e)

    def post_results(self):
        pass

    def tldt(self):
        self.checkout_code()
        self.setup_environment()
        self.run_tests()
        self.run_parsers()
        self.post_results()

main = Project
