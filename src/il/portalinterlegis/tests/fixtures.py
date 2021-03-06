# -*- coding: utf-8 -*-
from integrationtestutils import BrowserAwareIntegrationTesting
from plone.app.testing import PLONE_FIXTURE, PloneSandboxLayer, applyProfile
from zope.component import provideAdapter
from zope.configuration import xmlconfig


class IlPortalinterlegis(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):

        configurationContext = xmlconfig.string("""\
        <configure xmlns="http://namespaces.zope.org/zope" xmlns:meta="http://namespaces.zope.org/meta">
        <meta:provides feature="disable-autoinclude" />
        </configure>
        """, context=configurationContext)

        # Load ZCML for this package
        import plone.app.theming
        xmlconfig.file('configure.zcml', plone.app.theming,
                       context=configurationContext)
        import five.grok
        xmlconfig.file('configure.zcml', five.grok,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', plone.formwidget.contenttree,
                       context=configurationContext)
        import il.portalinterlegis
        xmlconfig.file('configure.zcml', il.portalinterlegis,
                       context=configurationContext)
        import collective.js.jqueryui
        xmlconfig.file('configure.zcml', collective.js.jqueryui,
                       context=configurationContext)

        #TODO: (fazer essa POG do jeito certo, que não sei qual é)
        # tive de repetir isso aqui pois não sei como esse adapter
        # é ativado normalmente, e como reproduzir isso no ambiente de teste
        from il.portalinterlegis.browser.boxes.manager import PersistentDictionaryField
        provideAdapter(PersistentDictionaryField)
        # fim da POG

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'il.portalinterlegis:default')


IL_PORTALINTERLEGIS_FIXTURE = IlPortalinterlegis()
IL_PORTALINTERLEGIS_INTEGRATION_TESTING = \
    BrowserAwareIntegrationTesting(bases=(IL_PORTALINTERLEGIS_FIXTURE, ),
                       name="IlPortalinterlegis:Integration")
