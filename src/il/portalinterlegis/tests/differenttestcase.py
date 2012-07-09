# -*- coding: utf-8 -*-
import codecs
import os
from itertools import count

import unittest2 as unittest


class DifferentTestCase(unittest.TestCase):
    """ Test case with differences output to temporary files
    """

    def __init__(self, *args):
        try:
            self.diff_counter = count(1)
            while True:
                f1, f2 = self._next_out_filenames()
                os.remove(f1)
                os.remove(f2)
        except OSError:
            pass
        self.diff_counter = count(1)
        super(DifferentTestCase, self).__init__(*args)

    def _next_out_filenames(self):
        base = "out_%s_%s" % (self.__class__.__name__, self.diff_counter.next())
        return ("%s.%s~" % (base, suffix) for suffix in ['first', 'second'])

    def assertMultiLineEqual(self, first, second, *args):
        """Same as standard assertMultiLineEqual,
        but outputs differing arguments to files names
        out_<couter>.1~ and
        out_<couter>.2~ where counter is an incrementing one."""

        if first is not None and second is not None and first != second:
            for fname, content in zip(self._next_out_filenames(), [first, second]):
                with codecs.open(fname, "w+", "utf-8") as f:
                    f.write(content)
        super(DifferentTestCase, self).assertMultiLineEqual(first, second, *args)


