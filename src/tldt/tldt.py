from __future__ import absolute_import
import contextlib
import importlib
import logging
import os
import subprocess

from tldt import git


logging.basicConfig(level=logging.INFO)


@contextlib.contextmanager
def chdir(dirname):
    cwd = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(cwd)


class Commenter(object):

    def __init__(self, github_user, github_password):

        self.general_errors = []
        self.general_warnings = []
        self.line_errors = []
        self.line_warnings = []

    def load_parser_results(self, parser):
        self.general_errors.extend(parser.general_errors)
        self.general_warnings.extend(parser.general_warnings)
        self.line_errors.extend(parser.line_errors)
        self.line_warnings.extend(parser.line_warnings)

    def _format_error_message(self, error):
        return "Error: %s" % error

    def _format_warning_message(self, warning):
        return "Warning: %s" % warning

    def _post_general_comment(self, comment):
        pass

    def _post_line_comment(self, comment):
        pass

    def post_comments(self):
        print "Got to posting comments"
        for error in self.general_errors:
            self._post_general_comment(error)

        for warning in self.general_warnings:
            self._post_general_comment(warning)

        for error in self.line_errors:
            self._post_line_comment(error)

        for warning in self.line_warnings:
            self._post_line_comment(warning)


class Project(object):

    def __init__(self, head_repo, head_sha, base_repo, base_sha,
                 config, comment):
        self.head_repo = head_repo
        self.head_sha = head_sha
        self.base_repo = base_repo
        self.base_sha = base_sha
        self.config = config
        self.comment = comment
        self.parsers = self.config.items("ActiveParsers")
        self.repo = None

    def checkout_code(self):
        local_checkout = self.config.get("repo", "local")
        logging.info("Checking out source code from %s to %s" % (self.base_repo, local_checkout))
        self.repo = git.Repo(local_checkout)
        self.repo.clone_or_update(self.base_repo)
        self.repo.fetch(self.head_repo)
        self.repo.checkout(self.head_sha)

    def setup_environment(self):
        logging.info("Running environment setup")
        with chdir(self.repo.local):
            subprocess.check_call(["build/setup_environment"])

    def run_tests(self):
        logging.info("Running tests")
        with chdir(self.repo.local):
            subprocess.check_call(["build/run_tests"])

    def run_parsers(self):
        logging.info("Running parsers")
        for parser_name, parser_module in self.parsers:
            logging.debug("Running parser %s" % parser_name)
            try:
                module = importlib.import_module(parser_module)
                kargs = dict(self.config.items("parser-%s" % parser_name))
                parser = module.Parser(**kargs)
                with chdir(self.repo.local):
                    parser.analyze()
                self.comment.load_parser_results(parser)
            except ImportError:
                logging.info("Could not load '%s' parsing module.Skipping...\n" % (parser_name))
            except Exception as e:
                logging.warning("Could not parse '%s'. Original traceback \n%r" % (parser_name, e))

    def post_results(self):
        logging.info("Posting results to Github pull request")
        self.comment.post_comments()

    def tldt(self):
        self.checkout_code()
        self.setup_environment()
        self.run_tests()
        self.run_parsers()
        self.post_results()
