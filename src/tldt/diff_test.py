from __future__ import absolute_import
import unittest

from tldt.diff import Mapper


DIFF = """diff --git a/requirements.txt b/requirements.txt
index 5dabd91..abbcf7c 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -1,4 +1,3 @@
 pygithub==1.11.1
 sh==1.08
-lxml==3.1.0
 pylint==0.26.0
diff --git a/src/tldt/diff.py b/src/tldt/diff.py
index 9a02f77..ce0f228 100644
--- a/src/tldt/diff.py
+++ b/src/tldt/diff.py
@@ -1,6 +1,7 @@
 import unidiff
 from cStringIO import StringIO
 import logging
+import sh # unused
 
 logger = logging.getLogger(__name__)
 
diff --git a/src/tldt/git_test.py b/src/tldt/git_test.py
index 797bcb6..6b71aba 100644
--- a/src/tldt/git_test.py
+++ b/src/tldt/git_test.py
@@ -17,6 +17,11 @@ def test_clone_and_checkout(self):
         repo = git.Repo(self.tmp_dir)
         repo.clone(self.tmp_repo_dir)
 
+    def test_fail(self):
+        # This test should always fail in order to
+        # test the tldt github pull request messaging
+        self.assertTrue(False)
+
     def tearDown(self):
         shutil.rmtree(self.tmp_dir)
 
diff --git a/src/tldt/tldt.py b/src/tldt/tldt.py
index 2960771..2e511dd 100644
--- a/src/tldt/tldt.py
+++ b/src/tldt/tldt.py
@@ -39,7 +39,6 @@ def __init__(self, github, pull_commit, pull_request, diff_factory):
         self.diff = diff_factory(pull_request.diff_url).text
         self.mapper = diff.Mapper(self.diff)
 
-
     def load_parser_results(self, parser):
         self.general_errors.extend(parser.general_errors)
         self.general_warnings.extend(parser.general_warnings)
@@ -121,10 +120,11 @@ def pull_request(self):
 
     def checkout_code(self):
         local_checkout = self.config.get("repo", "local")
-        logging.info("Checking out source code from %s to %s" % (self.base_repo, local_checkout))
+        logging.info("Fetching source from code from %s to %s" % (self.base_repo, local_checkout))
         self.repo = git.Repo(local_checkout)
         self.repo.clone_or_update(self.base_repo)
         self.repo.fetch(self.head_repo)
+        logging.info("Checking out source code from %s to %s" % (self.base_repo, local_checkout))
         self.repo.checkout(self.head_sha)
 
     def setup_environment(self):
"""


class TestMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = Mapper(DIFF)

    def test_mapping(self):
        self.assertIn("requirements.txt", self.mapper._map)

    def test_file_to_diff(self):
        linum = self.mapper.file_to_diff("src/tldt/diff.py", 4)
        self.assertEqual(linum, 4)
        linum = self.mapper.file_to_diff("requirements.txt", 3)
        self.assertEqual(linum, None)  # context line
        linum = self.mapper.file_to_diff("src/tldt/tldt.py", 124)
        self.assertEqual(linum, 13)


if __name__ == '__main__':
    unittest.main()
