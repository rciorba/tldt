from __future__ import absolute_import
import unittest
from cStringIO import StringIO

from tldt.diff import Mapper


DIFF = """diff --git a/docs/tldt.ini b/docs/tldt.ini
index ce9563d..aaed168 100644
--- a/docs/tldt.ini
+++ b/docs/tldt.ini
@@ -9,4 +9,7 @@ repo_name = django
 xunit = tldt.parsers.xunit
 
 [parser-xunit]
-file = output.xml
\ No newline at end of file
+file = output.xml
+
+[repo]
+local = /home/rciorba/repos/tltd_new
"""


class TestMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = Mapper(StringIO(DIFF))

    def test_mapping(self):
        self.assertIn("docs/tldt.ini", self.mapper._map)

    def test_file_to_diff(self):
        linum = self.mapper.file_to_diff("docs/tldt.ini", 15)
        self.assertEqual(linum, 14)


if __name__ == '__main__':
    unittest.main()
