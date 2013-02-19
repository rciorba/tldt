import tempfile
import unittest
import shutil
import git


# pylint: disable=W0703,R0904,W0201
class TestGit(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='gittest')

    def test_spam(self):
        repo = git.Repo(self.tmp_dir)
        repo.clone("/home/rciorba/repos/tldt/.git")
        repo.checkout('32bbf2dfc2de17fd10d665490d970960c3305bd2')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
