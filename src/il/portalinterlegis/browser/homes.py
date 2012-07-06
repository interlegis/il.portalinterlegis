# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import count

from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok

from boxes.carousel import CarouselBox, ProductsAndServices
from boxes.interfaces import ISuperTitleBox, ICalendar, IAcompanheOInterlegis, IHighlight, IRelated
from boxes.manager import DtRow, Box, GridView
from boxes.tabs import Tab, TabbedPane
from interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao


# These are meant for more readable grid definitions. Do not overuse.
FULL = 16
_count_dict = defaultdict(count)
def _(interface):
    return Box(interface, _count_dict[interface].next())
___ = DtRow

class Home(GridView):
    grok.name('home')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        ___((10, CarouselBox(0)), (6, _(ICalendar)),),
        ___((FULL, TabbedPane(
            Tab(u'Informação',  u'Informação Legislativa',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, ProductsAndServices(0)),),
            Tab(u'Capacitação', u'Capacitação Legislativa',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)),),
            Tab(u'Tecnologia',  u'Tecnologia Legislativa',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)),),
            Tab(u'Comunicação', u'Comunicação Legislativa',
                (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)), (4, _(IRelated)),),
            ))),
        ___((FULL, _(IAcompanheOInterlegis)), ),
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
