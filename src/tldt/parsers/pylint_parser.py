import tldt.parsers


class Parser(tldt.parsers.Parser):

    def __init__(self, *args, **kwargs):
        self.file = kwargs.pop("file")
        super(Parser, self).__init__(*args, **kwargs)

    def analyze(self):
        with open(self.file) as fh:
            self._parse_content(fh.xreadlines())

    def _parse_content(self, content):
        for line in content:
            fname, linum, msg = line.split(":", 2)
            self.line_error(fname, linum, msg)
