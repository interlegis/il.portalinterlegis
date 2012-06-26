# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import IPloneSiteRoot
from boxes.carousel import CarouselBox
from boxes.interfaces import ISimpleBox, ICalendar, IAcompanheOInterlegis, IHighlight
from boxes.manager import DtRow, Box, GridView
from boxes.tabs import Tab, TabbedPane
from five import grok
from interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao


# These are meant for more legible grid definitions. Do not overuse.
FULL = 16
___, _ = DtRow, Box


class Home(GridView):
    grok.name('home')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        ___((10, CarouselBox()), (6, _(ICalendar, 1)),),
        ___((FULL, TabbedPane(
            Tab(u'Informação',  u'Informação Legislativa',
                (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)),),
            Tab(u'Capacitação', u'Capacitação Legislativa',
                (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)),),
            Tab(u'Tecnologia',  u'Tecnologia Legislativa',
                (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)),),
            Tab(u'Comunicação', u'Comunicação Legislativa',
                (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)), (4, _(IHighlight, 1)),),
            ))),
        ___((FULL, _(IAcompanheOInterlegis, 1)), ),
        ___((4, _(IHighlight, 1)), (4, _(ISimpleBox, 1)), (4, _(ISimpleBox, 2)), (4, _(ISimpleBox, 3)),),
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
