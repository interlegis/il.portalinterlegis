# -*- coding: utf-8 -*-
from mock import patch

from il.portalinterlegis.browser.boxes.manager import Box, DtRow
from mock import MagicMock as Mock

from differenttestcase import DifferentTestCase

class TestUnitBoxes(DifferentTestCase):
    """ Unit tests for the boxes functionality
    """

    def test_box_render_basic(self):

        with patch('il.portalinterlegis.browser.boxes.manager.template_factory', TemplateFactoryStub()):

            box = Box(IStubBox, 1)
            box.content = Mock(return_value={'var': 'XXXX'})
            context = object()
            self.assertMultiLineEqual('''
<div id="IStubBox_1">
  XXXX
</div>
'''.strip('\n'), box(context))
            box.content.assert_called_with(context)

    def test_box_render_editable(self):
        with patch('il.portalinterlegis.browser.boxes.manager.template_factory', TemplateFactoryStub()):
            with patch('il.portalinterlegis.browser.boxes.manager.getSecurityManager') as security_mock:
                security_mock.checkPermission.return_value = True

                box = Box(IStubBox, 1)
                box.content = Mock(return_value={'var': 'XXXX'})
                context = object()
                self.assertMultiLineEqual('''
<div id="IStubBox_1" class ="editable-box" >
  XXXX
  <a class="editable-box-link" href="box_IStubBox_1">
    <img src="pencil_icon.png" width="16" height="16" alt="Edite esta caixa"/>
  </a>
</div>
'''.strip('\n'), box(context))
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
'''.strip('\n'), DtRow((1, Mock(return_value="AAA")),
           (2, Mock(return_value="BBB")),
           (3, Mock(return_value="CCC")),
           (1, Mock(return_value="DDD"))).render(context))


class IStubBox(object):
    pass

from il.portalinterlegis.browser.boxes.manager import template_factory, BaseBox
from jinja2 import Template


class TemplateFactoryStub(object):

    def get_template(self, name):
        if name == "istubbox.html":
            return Template("{{var}}")
        elif name == "basebox.html":
            return template_factory.get_template(name)
        else:
            raise AssertionError("Unexpected name: [%s]" % name)
