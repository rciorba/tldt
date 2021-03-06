class Parser(object):

    def __init__(self):
        self.general_errors = []
        self.general_warnings = []
        self.line_errors = []
        self.line_warnings = []

    def general_error(self, error_message):
        self.general_errors.append(error_message)

    def general_warning(self, warning_message):
        self.general_warnings.append(warning_message)

    def line_error(self, filename, lineno, error_message):
        self.line_errors.append((filename, lineno, error_message))

    def line_warning(self, filename, lineno, warning_message):
        self.line_warnings.append((filename, lineno, warning_message))

    def analyze(self):
        raise NotImplementedError()
