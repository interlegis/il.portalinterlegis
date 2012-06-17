# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from content.createcontent import createObjects
from browser.homes import IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile('il.portalinterlegis.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    # home
    if hasattr(portal, 'front-page'):
        del portal['front-page']
    portal.setLayout('home')

    # navegacao de 1o nivel
    normalizer = getUtility(IIDNormalizer)
    folders_do_menu = [{'id': normalizer.normalize(title),
                     'title': title,
                     'description': u'Seção %s' % title,
                     'type': 'Folder',
                     'workflow_transition': 'publish',
                     'exclude_from_nav': False,
                     'layout': 'home',
                     'marker_interface': marker}
                     for title, marker in [
                             (u'Comunidade Legislativa', IComunidadeLegislativa),
                             (u'Informação', IInformacao),
                             (u'Capacitação', ICapacitacao),
                             (u'Tecnologia', ITecnologia),
                             (u'Comunicação', IComunicacao),
                             ]]
    createObjects(portal, folders_do_menu)

    # esconde todo o resto
    ids_folders_do_menu = [f['id'] for f in folders_do_menu] + ['front-page']
    for id in portal.objectIds():
        if id not in ids_folders_do_menu:
            obj = portal[id]
            if hasattr(obj, 'exclude_from_nav'):
                obj.setExcludeFromNav(True)
                obj.reindexObject()  # nao sei exatamente pq isso, mas nao custa colocar
