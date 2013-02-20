import unidiff


class Mapper(object):

    def __init__(self, diff_file):
        self.diff = unidiff.parser.parse_unidiff(diff_file)
        self._map = {}
        for index, file_ in enumerate(self.diff, 1):
            file_name = file_.target_file[2:].strip()  # remove "b/" and trailing "\n"
            self._map[file_name] = file_, index

    def file_to_diff(self, filename, linum):
        f, f_index = self._map.get(filename, (None, None))
        if f is None:
            return None
        diff_line = 2 + f_index * 2  # account for file lines in diff
        for hunk in f:
            diff_line += hunk.length + 1  # account for hunk range info
            start = hunk.target_start + hunk.start_context
            # -1 because first line of hunk is at target_start
            end = hunk.target_start + hunk.target_length - 1 - hunk.end_context
            if start <= linum <= end:
                return diff_line
