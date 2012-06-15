# -*- coding: utf-8 -*-
import unittest2 as unittest
from mock import patch

from il.portalinterlegis.browser.boxes.manager import Box, DtRow
from itertools import count
from mock import MagicMock as Mock

diff_count = count(1)

class TestUnitBoxes(unittest.TestCase):
    """ Unit tests for the boxes functionality
    """

    def setUp(self):
        pass

    def assertMultiLineEqual(self, first, second, *args):
        "ignores differences in leading and trailing whitespace in strings"
        self.assert_(isinstance(first, basestring), (
                'First argument is not a string'))
        self.assert_(isinstance(second, basestring), (
                'Second argument is not a string'))

        first = first.strip()
        second = second.strip()
        if first != second:
            c = diff_count.next()
            for i, s in enumerate([first, second]):
                with open("out_%s.%s" % (c, i), "w+") as f:
                    f.write(s)
        super(TestUnitBoxes, self).assertMultiLineEqual(first, second, *args)

    def test_box_render_basic(self):

        with patch('il.portalinterlegis.browser.boxes.manager.template_factory',
                   template_factory_stub('        XXXX')):

            box = Box(IStubBox, 1)
            box.content = Mock(
                return_value = {'var': 'XXXX'})
            context = object()
            self.assertMultiLineEqual('''
      <div id="IStubBox_1">
        XXXX
      </div>''', box(context))
            box.content.assert_called_with(context)

    def test_box_render_editable(self):
        with patch('il.portalinterlegis.browser.boxes.manager.template_factory',
                   template_factory_stub('        XXXX')):
            with patch('il.portalinterlegis.browser.boxes.manager.getSecurityManager') as security_mock:
                security_mock.checkPermission.return_value = True

                box = Box(IStubBox, 1)
                box.content = Mock(
                    return_value = {'var': 'XXXX'})
                context = object()
                self.assertMultiLineEqual('''
      <div id="IStubBox_1" class ="editable-box">
        XXXX
      </div>''', box(context))
                box.content.assert_called_with(context)

    def test_row_structure(self):
        context = object()

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
''', DtRow((1, Mock(return_value="\n      AAA")),
           (2, Mock(return_value="\n      BBB")),
           (3, Mock(return_value="\n      CCC")),
           (1, Mock(return_value="\n      DDD"))).render(context))


class IStubBox(object):
    pass

class TemplateStub(object):
    def render(self, context):
        return "        %(var)s" % context

def template_factory_stub(value):
    template_factory_stub = Mock()
    template_factory_stub.get_template.return_value = TemplateStub()
    return template_factory_stub

