from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok

from boxes.manager import GridView
from interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao
from boxes.interfaces import \
     ISimpleBox, ICarousel, ICalendar, ITabsPilares, IAcompanheOInterlegis, IHighlight

FULL = 16

class Home(GridView):
    grok.name('home')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        [(10, ICarousel, 1), (6, ICalendar, 1)],
        [(FULL, ITabsPilares, 1)],
        [(FULL, IAcompanheOInterlegis, 1)],
        [(4, IHighlight, 1), (4, ISimpleBox, 1), (4, ISimpleBox, 2), (4, ISimpleBox, 3)]
    ]

class Carousel(GridView):
    grok.name('carrossel')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    grid = [
        [(10, ICarousel, 1), (6, ICalendar, 1)],
        [(10, ICarousel, 2), (6, ICalendar, 2)],
        [(10, ICarousel, 3), (6, ICalendar, 3)],
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

