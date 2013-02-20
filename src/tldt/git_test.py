import tempfile
import unittest
import shutil
import git


# pylint: disable=W0703,R0904,W0201
class TestGit(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='gittest')
        self.tmp_repo_dir = tempfile.mkdtemp(prefix="gitrepo")
        self.repo = git.Repo(self.tmp_repo_dir)
        self.repo.git.init()

    def test_clone_and_checkout(self):
        repo = git.Repo(self.tmp_dir)
        repo.clone(self.tmp_repo_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
