# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import count

from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok
from interfaces import \
     IComunidadeLegislativa, IInformacao, ICapacitacao, ITecnologia, IComunicacao

from boxes import colab, socialnetworks, video, Events, interlegis_na_midia, noticias_e_artigos_interlegis, consultoria_e_informacao, produtos_de_tecnologia, capacitacao_ilb, relacionamento
from boxes.carousel import CarouselBox
from boxes.manager import DtRow, Box, GridView
from boxes.simplerow import SimpleRow


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
        ___((10, CarouselBox(0)), (6, Events()),),

        ___((8, interlegis_na_midia), (8, noticias_e_artigos_interlegis),),
        ___((FULL, SimpleRow(u'Produtos e serviços interlegis',
                            (4, consultoria_e_informacao), (4, produtos_de_tecnologia), (4, capacitacao_ilb), (4, relacionamento)))), 

        ___((FULL, SimpleRow(u'Acompanhe o Interlegis',
                            (6, colab), (5, socialnetworks), (5, video)))), 

        # TODO linha tirada por falta de uso. Sera trocada por um linha com info do SIGI
        # ___((4, _(IHighlight)), (4, _(ISuperTitleBox)), (4, _(ISuperTitleBox)), (4, _(ISuperTitleBox)),),
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
