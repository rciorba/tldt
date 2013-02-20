import unittest

import tldt.parsers.xunit

PASSED_TEST = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuite>
<testcase classname="test.Test" name="meh" time="0.00" />
</testsuite>
"""

FAILED_TEST = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuite>
<testcase classname="test.Test" name="meh" time="0.00">
<failure>
  Failed assertions here
</failure>
</testcase>
</testsuite>
"""

ERROR_TEST = """\
<?xml version="1.0" encoding="UTF-8"?>
<testsuite>
<testcase classname="test.Test" name="meh" time="0.00">
<error>
  Tracebacks here
</error>
</testcase>
</testsuite>
"""


class XUnitTest(unittest.TestCase):

    def setUp(self):
        super(XUnitTest, self).setUp()
        self.parser = tldt.parsers.xunit.Parser(file="/dev/null")
        print id(self.parser)
        self.assert_no_errors_or_warnings()

    def assert_no_errors(self):
        self.assertEqual(len(self.parser.general_errors), 0)
        self.assertEqual(len(self.parser.line_errors), 0)

    def assert_no_warnings(self):
        self.assertEqual(len(self.parser.general_warnings), 0)
        self.assertEqual(len(self.parser.line_warnings), 0)

    def assert_no_errors_or_warnings(self):
        self.assert_no_warnings()
        self.assert_no_errors()

    def test_no_errors_reported(self):
        self.parser._parse_content(PASSED_TEST)
        self.assert_no_errors_or_warnings()

    def test_errors_reported(self):
        self.parser._parse_content(ERROR_TEST)
        self.assertEqual(len(self.parser.general_errors), 1)
        self.assert_no_warnings()

    def test_failures_reported(self):
        self.parser._parse_content(FAILED_TEST)
        self.assertEqual(len(self.parser.general_errors), 1)
        self.assert_no_warnings()
