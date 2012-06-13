# -*- coding: utf-8 -*-
import lxml.html
import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from fixtures import IL_PORTALINTERLEGIS_INTEGRATION_TESTING
from plone.testing.z2 import Browser
from zExceptions import NotFound
from plone.app.testing import login, SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from il.portalinterlegis.browser.boxes import BoxManager
from il.portalinterlegis.browser.interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao, \
     ISimpleBox


class TestIntegracao(unittest.TestCase):

    layer = IL_PORTALINTERLEGIS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def new_browser(self, path=None, as_admin=False):
        browser = Browser(self.app)
        browser.handleErrors = False
        if as_admin:
            browser.open(self.url("login_form"))
            browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
            browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
            browser.getControl(name='submit').click()
        browser.open(self.url(path))
        return browser

    def dom(self, browser):
        return lxml.html.fromstring(browser.contents)

    def url(self, path=None):
        base = self.portal.absolute_url()
        if path:
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
        browser = self.new_browser()
        dom = self.dom(browser)
        self.assertEqual([u'O Interlegis',
                          u'Comunidade Legislativa',
                          u'Informação',
                          u'Capacitação',
                          u'Tecnologia',
                          u'Comunicação',],
            [li.text_content() for li in dom.cssselect('#portal-globalnav li')])

    def test_homes_marcadas_e_com_layout_home(self):
        for id, marker in [('comunidade-legislativa', IComunidadeLegislativa),
                           ('informacao',          IInformacao),
                           ('capacitacao',         ICapacitacao),
                           ('tecnologia',          ITecnologia),
                           ('comunicacao',         IComunicacao),
                           ]:
            obj = self.portal[id]
            self.assertTrue(marker.providedBy(obj))
            self.assertEqual('home', obj.getLayout())

    def test_box_content_is_empty_before_visiting_form(self):
        self.assertEqual({}, BoxManager(ISimpleBox).box_content(self.portal, 1))

    def test_using_box_form_creates_box_content(self):
        context = self.portal
        boxmanager = BoxManager(ISimpleBox)

        def use_box_form(title, subtitle, text, num):
            browser = self.new_browser(boxmanager._box_name_for_url(num), as_admin=True)
            browser.getControl(name='form.widgets.title').value = title
            browser.getControl(name='form.widgets.subtitle').value = subtitle
            browser.getControl(name='form.widgets.text').value = text
            browser.getControl(name='form.buttons.apply').click()

        use_box_form('TIT_1', 'SUBTIT_1', 'TEXT_1', 1)
        use_box_form('TIT_2', 'SUBTIT_2', 'TEXT_2', 2)
        self.assertEqual({'title': 'TIT_1', 'subtitle': 'SUBTIT_1', 'text': 'TEXT_1'},
                         boxmanager.box_content(context, 1))
        self.assertEqual({'title': 'TIT_2', 'subtitle': 'SUBTIT_2', 'text': 'TEXT_2'},
                         boxmanager.box_content(context, 2))

    def test_box_forms_numbers_begin_from_1_not_zero(self):
        with self.assertRaises(NotFound):
            browser = self.new_browser(BoxManager(ISimpleBox)._box_name_for_url(0), as_admin=True)

    def test_box_forms_are_limited(self):
        with self.assertRaises(NotFound):
            browser = self.new_browser(BoxManager(ISimpleBox)._box_name_for_url(1000000), as_admin=True)

    def test_box_form_cannot_be_created_after_initialization(self):
        BoxManager(ISimpleBox).build_form(99) # try to build a box form in an arbitrary moment
        with self.assertRaises(NotFound):
            browser = self.new_browser(BoxManager(ISimpleBox)._box_name_for_url(99), as_admin=True)

