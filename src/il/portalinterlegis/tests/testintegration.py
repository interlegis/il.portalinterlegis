# -*- coding: utf-8 -*-
import lxml.html
import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from zExceptions import NotFound

from fixtures import IL_PORTALINTERLEGIS_INTEGRATION_TESTING
from il.portalinterlegis.browser.boxes.interfaces import ISuperTitleBox
from il.portalinterlegis.browser.boxes.manager import \
     Box, build_box_form, NUMBER_OF_PRE_CREATED_BOXES
from il.portalinterlegis.browser.interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao


class TestIntegracao(unittest.TestCase):

    layer = IL_PORTALINTERLEGIS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def dom(self, browser):
        return lxml.html.fromstring(browser.contents)

    def url(self, path=None):
        base = self.portal.absolute_url()
        if path:
            path.strip('/')
            return '%s/%s' % (base, path)
        else:
            return base

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'il.portalinterlegis'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_tabs_na_home(self):
        browser = self.layer.anonymous_browser()
        browser.open(self.url())
        dom = self.dom(browser)
        self.assertEqual([u'O Interlegis',
                          u'Comunidade Legislativa',
                          u'Informação',
                          u'Capacitação',
                          u'Tecnologia',
                          u'Comunicação'],
            [li.text_content() for li in dom.cssselect('#portal-globalnav li')])

    def test_homes_marcadas_e_com_layout_home(self):
        for id, marker in [('comunidade-legislativa', IComunidadeLegislativa),
                           ('informacao', IInformacao),
                           ('capacitacao', ICapacitacao),
                           ('tecnologia', ITecnologia),
                           ('comunicacao', IComunicacao),
                           ]:
            obj = self.portal[id]
            self.assertTrue(marker.providedBy(obj))
            self.assertEqual('home', obj.getLayout())

    # BOXES

    def test_box_content_is_empty_before_visiting_form(self):
        self.assertEqual({}, Box(ISuperTitleBox, 1).get_data(self.portal))

    def test_using_box_form_creates_box_content(self):
        context = self.portal

        def use_box_form(supertitle, title, text, target, box):
            browser = self.layer.manager_browser()
            browser.open(self.url(box.form_name))
            browser.getControl(name='form.widgets.supertitle').value = supertitle
            browser.getControl(name='form.widgets.title').value = title
            browser.getControl(name='form.widgets.text').value = text
            # TODO: nao sei como testar um AutocompleteFieldWidget com o zope.testbrowser (tem javascript)
            # browser.getControl(label=u'Conteúdo relacionado').value = target
            browser.getControl(name='form.buttons.apply').click()

        box_1 = Box(ISuperTitleBox, 1)
        use_box_form('SUPERTIT_1', 'TIT_1', 'TEXT_1', 'ALVO_1', box_1)
        self.assertEqual(dict(supertitle='SUPERTIT_1', title='TIT_1', text='TEXT_1', target=None, image=None),
                         box_1.get_data(context))

        # a second one to test there is no mutual interference
        box_2 = Box(ISuperTitleBox, 2)
        use_box_form('SUPERTIT_2', 'TIT_2', 'TEXT_2', 'ALVO_2', box_2)
        self.assertEqual(dict(supertitle='SUPERTIT_2', title='TIT_2', text='TEXT_2', target=None, image=None),
                         box_2.get_data(context))

    def test_box_forms_are_limited(self):
        browser = self.layer.manager_browser()
        # These are ok. No exception raised
        browser.open(self.url(Box(ISuperTitleBox, 0).form_name))
        browser.open(self.url(Box(ISuperTitleBox,
                                  NUMBER_OF_PRE_CREATED_BOXES - 1).form_name))
        with self.assertRaises(NotFound):
            # This doesn't exist
            browser.open(self.url(Box(ISuperTitleBox,
                                      NUMBER_OF_PRE_CREATED_BOXES).form_name))

    def test_box_form_cannot_be_created_after_initialization(self):
        """Try to build a box form in an arbitrary moment.
           Unfortunately that's not possible.
        """
        build_box_form(Box(ISuperTitleBox, 99))
        with self.assertRaises(NotFound):
            browser = self.layer.manager_browser()
            browser.open(self.url(Box(ISuperTitleBox, 99).form_name))

    # CAROUSEL

    def test_carousel(self):
        """Carousel editing happy path.
        """
        #
        # got carousel page, relative to a given "base page"
        # there are 5 visible carousel slots each
        #   with its own "selected" checkbox
        # put data in the first 4 of them
        #   with only the 1st, 3rd and 4th selected
        # save
        # go to the "base page" and assert that there is a carousel with 3 panels
        #   they match the panels number 1, 3 and 4


