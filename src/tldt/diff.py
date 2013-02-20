import unidiff


class Mapper(object):

    def __init__(self, diff_file):
        self.diff = unidiff.parser.parse_unidiff(diff_file)
        self._map = {}
        for index, file_ in enumerate(self.diff, 1):
            self._map[file_.target_path[2:]] = file_, index

    def file_to_diff(self, filename, linum):
        f, f_index = self._map.get(filename, None)
        if f is None:
            return None
        diff_line = 2 + f_index * 2  # account for file lines in diff
        for hunk in f:
            diff_line += hunk.length + 1  # account for hunk range info
            start = hunk.target_start + hunk.context
            end = hunk.target_start + hunk.target_length - hunk.context
            if start <= linum <= end:
                return diff_line
