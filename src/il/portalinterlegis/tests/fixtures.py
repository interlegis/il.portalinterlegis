# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from plone.app.testing import PLONE_FIXTURE, PloneSandboxLayer, IntegrationTesting, applyProfile
from z3c.form import datamanager
from z3c.form.interfaces import IDataManager
from zope.component import adapts, provideAdapter
from zope.configuration import xmlconfig
from zope.interface import implements
from zope.schema.interfaces import IField
from integrationtestutils import BrowserAwareIntegrationTesting

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
        xmlconfig.file('configure.zcml',
                       plone.app.theming,
                       context=configurationContext)
        import five.grok
        xmlconfig.file('configure.zcml',
                       five.grok,
                       context=configurationContext)
        import il.portalinterlegis
        xmlconfig.file('configure.zcml',
                       il.portalinterlegis,
                       context=configurationContext)

        #TODO: (fazer essa POG do jeito certo, que não sei qual é)
        # tive de repetir isso aqui pois não sei como esse mesmo trecho
        # (de browser.boxes) é ativado normalmente, e como reproduzir isso no ambiente de teste
        class PersistentDictionaryField(datamanager.DictionaryField):
            adapts(PersistentDict, IField)
            implements(IDataManager)
        provideAdapter(PersistentDictionaryField)
        # fim da POG

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'il.portalinterlegis:default')


IL_PORTALINTERLEGIS_FIXTURE = IlPortalinterlegis()
IL_PORTALINTERLEGIS_INTEGRATION_TESTING = \
    BrowserAwareIntegrationTesting(bases=(IL_PORTALINTERLEGIS_FIXTURE, ),
                       name="IlPortalinterlegis:Integration")
