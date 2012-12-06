# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

grupo_pilar = {"SACL": u"informação", "SFCO": u"informação", "SPPE": u"informação",
               "SCLE": u"capacitação",
               "SSTIN": u"tecnologia", "SEIT": u"tecnologia",
               # a comunicação é uma  exceção
               # "SSFAC": u"comunicação",
               }

def categoriza_noticia(context, noticia):
    autor = noticia.Creators()[0]
    groups_tool = getToolByName(context, 'portal_groups')
    grupos_do_autor = set(map(str, groups_tool.getGroupsByUserId(autor)))
    grupos_relevantes = grupos_do_autor.intersection(set(grupo_pilar))
    if grupos_relevantes:
        pilar = grupo_pilar[grupos_relevantes.pop()]
        categorias = set(noticia.Subject())
        categorias.add(pilar)
        noticia.setSubject(tuple(categorias))

portal.portal_catalog(created = {'query': DateTime('2012-11-01'), 'range': 'min'}, portal_type="News Item")

for brain in busca:
    categoriza_noticia(portal, brain.getObject())
