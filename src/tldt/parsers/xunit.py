from lxml import etree

import tldt.parsers


class Parser(tldt.parsers.Parser):

    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop("file")

    def analyze(self):
        with open(self.file) as fh:
            self._parse_content(fh.read())

    def _parse_content(self, content):
        results = etree.from_string(content)
        if results.findall("failure"):
            self.general_error("Tests failed")
