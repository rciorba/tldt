import unidiff
from cStringIO import StringIO
import logging

logger = logging.getLogger(__name__)


class Mapper(object):

    def __init__(self, diff_file):
        self.diff = unidiff.parser.parse_unidiff(StringIO(diff_file))
        self._map = {}
        for file_ in self.diff:
            file_name = file_.target_file[2:].strip()  # remove "b/" and trailing "\n"
            self._map[file_name] = file_

    def file_to_diff(self, filename, linum):
        f = self._map.get(filename, None)
        if f is None:
            return None
        hunk_offset = 0
        for hunk in f:
            start = hunk.target_start
            end = hunk.target_start + hunk.target_length - 1
            if not(start <= linum <= end):
                hunk_offset += len(hunk.original_lines) + 1  # account for hunk header
                continue
            offset = linum - hunk.target_start
            final_line = offset + 1
            if hunk.original_types[offset] == '+':
                return final_line + hunk_offset
