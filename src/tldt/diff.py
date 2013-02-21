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
            logger.info("ignoring error at %s:%s" % (filename, linum))
            return None
        diff_line = 0
        for hunk in f:
            diff_line += hunk.length + 1  # account for hunk range info
            start = hunk.target_start + hunk.start_context
            # -1 because first line of hunk is at target_start
            end = hunk.target_start + hunk.target_length - 1 - hunk.end_context
            if start <= linum <= end:
                return diff_line
