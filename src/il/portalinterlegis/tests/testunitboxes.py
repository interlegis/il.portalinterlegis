# -*- coding: utf-8 -*-
import unittest2 as unittest
from mock import patch

from il.portalinterlegis.browser.boxes.manager import BoxManager, DtRow
from il.portalinterlegis.browser.boxes.interfaces import ISimpleBox
from mockutils import *
from itertools import count

_any_ = None # anything, doesn't really matter

class TestUnitBoxes(unittest.TestCase):
    """ Unit tests for the boxes functionality
    """

    def setUp(self):
        self.diff_count = count(1)

    def assertMultiLineEqual(self, first, second, *args):
        "ignores differences in leading and trailing whitespace in strings"
        self.assert_(isinstance(first, basestring), (
                'First argument is not a string'))
        self.assert_(isinstance(second, basestring), (
                'Second argument is not a string'))

        first = first.strip()
        second = second.strip()
        if first != second:
            c = self.diff_count.next()
            for i, s in enumerate([first, second]):
                with open("out_%s.%s" % (c, i), "w+") as f:
                    f.write(s)
        super(TestUnitBoxes, self).assertMultiLineEqual(first, second, *args)

    def test_html(self):
        with patch.object(BoxManager, 'box_content') as mock:
            mock.return_value = {'title': 'TIT_1', 'subtitle': 'SUBTIT_1', 'text': 'TEXT_1', 'target': 'alvo'}

            boxmanager = BoxManager(ISimpleBox)
            self.assertMultiLineEqual('''
      <div class="simple-box">
        <a href="/portal/alvo">
          <h2>TIT_1</h2>
          <h3 class="icon-news">SUBTIT_1</h3>
          <p>
            TEXT_1
          </p>
        </a>
      </div>
        ''', boxmanager.html(_any_, _any_))

    def test_row(self):
        context = object()
        def mock_template(c):
            # A template is just a callable. A function will do.
            def f(context):
                return "\n      %s" % (3*c)
            return f

        self.assertMultiLineEqual('''
  <div class="dt-row">
    <div class="dt-cell dt-position-0 dt-width-1">
      AAA
    </div>
    <div class="dt-cell dt-position-1 dt-width-2">
      BBB
    </div>
    <div class="dt-cell dt-position-3 dt-width-3">
      CCC
    </div>
    <div class="dt-cell dt-position-6 dt-width-1">
      DDD
    </div>
  </div>
''', DtRow((1, mock_template('A')),
           (2, mock_template('B')),
           (3, mock_template('C')),
           (1, mock_template('D'))).render(context))


