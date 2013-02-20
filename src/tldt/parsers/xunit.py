from lxml import etree

import tldt.parsers


class Parser(tldt.parsers.Parser):

    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop("file")
        super(Parser, self).__init__(*args, **kwargs)

    def analyze(self):
        with open(self.file) as fh:
            self._parse_content(fh.read())

    def _parse_content(self, content):
        results = etree.fromstring(content)
        if len(results.findall("testcase/failure")) > 0:
            self.general_error("Tests failed")
        if len(results.findall("testcase/error")) > 0:
            self.general_error("Tests had errors")
