import contextlib
import ConfigParser
import importlib
import os
import subprocess


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
        self.root_dir = None
        # FOOBAR
        self.tldt()

    def checkout_code(self):
        self.root_dir = "/path/to/code_chekout"

    def setup_environment(self):
        with chdir(self.root_dir):
            subprocess.check_call(["build/setup_environment"])

    def run_tests(self):
        with chdir(self.root_dir):
            subprocess.check_call(["build/run_tests"])

    def run_parsers(self):
        for parser_name, parser_module in self.parsers:
            try:
                module = importlib.import_module(parser_module)
                kargs = dict(self.config.items("parser-%s" % parser_name))
                module.Parser(**kargs)
            except ImportError as e:
                print "Could not load '%s' parsing module.\n %r " % (parser_name, e)

    def post_results(self):
        pass

    def tldt(self):
        self.checkout_code()
        #self.setup_environment()
        #self.run_tests()
        self.run_parsers()
        self.post_results()

main = Project
