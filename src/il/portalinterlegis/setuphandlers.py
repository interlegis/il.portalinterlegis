# -*- coding: utf-8 -*-
from content.createcontent import createObjects


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

    # cria objetos obrigatorios
    createObjects(portal, [{'id': 'interlegisnamidia',
                            'title': u'Interlegis na Mídia',
                            'description': u'Notícias e novidades sobre o Programa Interlegis na Mídia',
                            'type': 'Folder',}])
