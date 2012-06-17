# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok

from boxes.interfaces import ISimpleBox, ICarousel, ICalendar, IAcompanheOInterlegis, IHighlight
from boxes.manager import DtRow, Box, GridView
from interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao


class Tab(object):

    def __init__(self, title, inner_title, *row_spec):
        self.title = title
        self.inner_title = inner_title
        self.row_spec = row_spec

    def __call__(self, context):
        return 'TODO: TAB %s' % self.title


class TabbedPane(object):

    def __init__(self, *tabs):
        self.tabs = tabs

    def __call__(self, context):
        return ''.join([tab(context) for tab in self.tabs])

# These are meant for more legible grid definitions. Do not overuse.
FULL = 16
___, _ = DtRow, Box


class Home(GridView):
    grok.name('home')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        ___((10, _(ICarousel, 1)), (6, _(ICalendar, 1)),),
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


class Carousel(GridView):
    grok.name('carrossel')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        ___((10, _(ICarousel, 1)), (6, _(ICalendar, 1)),),
        ___((10, _(ICarousel, 2)), (6, _(ICalendar, 2)),),
        ___((10, _(ICarousel, 3)), (6, _(ICalendar, 3)),),
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
