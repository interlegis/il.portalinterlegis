# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import count

from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok

from boxes import colab, LastNews, socialnetworks, video
from boxes.carousel import CarouselBox, ProductsAndServices
from boxes.interfaces import ISuperTitleBox, ICalendar, IHighlight, IRelated
from boxes.manager import DtRow, Box, GridView
from boxes.simplerow import SimpleRow
from boxes.tabs import Tab, TabbedPane
from interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao


# These are meant for more readable grid definitions. Do not overuse.

def _(interface):
    return Box(interface, _count_dict[interface].next())

___ = DtRow

_count_dict = defaultdict(count)

FULL = 16


class Home(GridView):
    grok.name('home')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        ___((10, CarouselBox(0)), (6, _(ICalendar)),),
        ___((FULL, TabbedPane(
            Tab('informacao', u'Informação', u'Informação',
                (4, _(IRelated)), (4, LastNews("informacao")), (4, _(IRelated)), (4, ProductsAndServices(0)),),
            Tab('capacitacao', u'Capacitação', u'Capacitação',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, ProductsAndServices(1)),),
            Tab('tecnologia', u'Tecnologia', u'Tecnologia',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, ProductsAndServices(2)),),
            Tab('comunicacao', u'Comunicação', u'Comunicação',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, ProductsAndServices(3)),),
            ))),
        ___((FULL, SimpleRow(u'Acompanhe o Interlegis',
                            (5, colab), (5, socialnetworks), (5, video)))),
        ___((4, _(IHighlight)), (4, _(ISuperTitleBox)), (4, _(ISuperTitleBox)), (4, _(ISuperTitleBox)),),
    ]


class ComunidadeLegislativaHome(grok.View):
    grok.name('home')
    grok.context(IComunidadeLegislativa)
    grok.require('zope2.View')


class InformacaoHome(grok.View):
    grok.name('home')
    grok.context(IInformacao)
    grok.require('zope2.View')


class CapacitacaoHome(grok.View):
    grok.name('home')
    grok.context(ICapacitacao)
    grok.require('zope2.View')


class TecnologiaHome(grok.View):
    grok.name('home')
    grok.context(ITecnologia)
    grok.require('zope2.View')


class ComunicacaoHome(grok.View):
    grok.name('home')
    grok.context(IComunicacao)
    grok.require('zope2.View')
