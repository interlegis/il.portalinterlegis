# -*- coding: utf-8 -*-
import unittest2 as unittest
from mock import patch

from il.portalinterlegis.browser.boxes import BoxManager, row_html
from il.portalinterlegis.browser.interfaces import ISimpleBox
from mockutils import *

_ = None # anything, doesn't really matter

class TestUnitBoxes(unittest.TestCase):
    """ Unit tests for the boxes functionality
    """

    def setUp(self):
        pass

    def assertEqual(self, first, second, *args):
        "ignores differences in leading and trailing whitespace in strings"
        super(TestUnitBoxes, self).assertMultiLineEqual(
            isinstance(first, str) and first.strip() or first,
            isinstance(second, str) and second.strip() or second, *args)

    def test_html(self):
        with patch.object(BoxManager, 'box_content') as mock:
            mock.return_value = {'title': 'TIT_1', 'subtitle': 'SUBTIT_1', 'text': 'TEXT_1'}

            boxmanager = BoxManager(ISimpleBox)
            self.assertEqual('''
      <div class="simple-box">
        <h2>TIT_1</h2>
        <h3 class="icon-news"><a href="">SUBTIT_1</a></h3>
        <p>
          TEXT_1
        </p>
      </div>
        ''', boxmanager.html(_, _))

    def test_row(self):
        context = object()
        with patch.object(BoxManager, 'html') as mock_html:
            with patch.object(BoxManager, '_box_key') as mock_box_key:

                @return_values(mock_html, ['\n      %s' % s for s in ['AAA', 'BBB', 'CCC', 'DDD']])
                def side_effect(c, n):
                    self.assertIs(context, c)

                from itertools import count
                numbers = count(1)
                @return_values(mock_box_key, [1, 2, 3, 4])
                def side_effect(n):
                    self.assertIs(numbers.next(), n)

                self.assertEqual('''
  <div class="dt-row">
    <div id="1" class=" dt-cell dt-position-0 dt-width-1">
      AAA
    </div>
    <div id="2" class=" dt-cell dt-position-1 dt-width-2">
      BBB
    </div>
    <div id="3" class=" dt-cell dt-position-3 dt-width-3">
      CCC
    </div>
    <div id="4" class=" dt-cell dt-position-6 dt-width-1">
      DDD
    </div>
  </div>
''', row_html(context, [(1, _, 1), (2, _, 2), (3, _, 3), (1, _, 4)] ))


