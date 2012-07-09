# -*- coding: utf-8 -*-

# Este arquivo contém trechos de código que podem ser usados para inspeção rápida no prompt

from zope.annotation import IAnnotations
aa = IAnnotations(context)['il.portalinterlegis.boxes']
aa['ISimpleBox_1']

from il.portalinterlegis.browser.boxes import BoxManager
from il.portalinterlegis.browser.interfaces import ISimpleBox
boxmanager = BoxManager(ISimpleBox)
boxmanager.box_content(context, 1)

from Testing.ZopeTestCase.utils import startZServer
startZServer()

with open("out", "w+") as f: f.write(browser.contents)


################################################################
 Fotografia de um estado das anotacoes da home
################################################################
{'IAcompanheOInterlegis_0': {},
 'IAcompanheOInterlegis_1': {},
 'ICalendar_0': {},
 'ICalendar_1': {},
 'ICalendar_2': {},
 'ICalendar_3': {},
 'ICarouselItem_0': {'image': u'/++theme++il.portalinterlegis/temp/images/1.jpg',
  'target': '/news/nova-noticia',
  'text': u'<p>aaaaaaaaaaaaa</p>',
  'title': u'Praia'},
 'ICarouselItem_1': {'image': u'/++theme++il.portalinterlegis/temp/images/caneca.jpg',
  'target': '/news/nova-noticia',
  'text': u'<p>aaaaaaaaaaaa</p>',
  'title': u'Mais uma'},
 'ICarouselItem_2': {'image': u'/++theme++il.portalinterlegis/temp/images/interlegis.jpg',
  'target': '/news/nova-noticia',
  'text': u'<p>BBBBB</p>',
  'title': u'Nova AAA'},
 'ICarouselItem_3': {'target': '/news/nova-noticia',
  'text': u'<p>Donec dui diam, bibendum eu tincidunt a, vehicula ac sem.</p>',
  'title': u'T\xc3\xadtulo <b>legal</b>'},
 'ICarouselItem_4': {'target': '/news/nova-noticia',
  'text': u'<p>Donec dui diam, bibendum eu tincidunt a, vehicula ac sem.</p>',
  'title': u'T\xc3\xadtulo <b>legal</b>'},
 'ICarousel_1': {},
 'ICarousel_2': {},
 'ICarousel_3': {},
 'IHighlight_0': {},
 'IHighlight_1': {},
 'IRelated_0': {'image': u'/++theme++il.portalinterlegis/temp/images/placeholder.gif',
  'target': '/news/nova-noticia',
  'text': u'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec odio et  dolor bibendum posuere ut at ante. Duis dictum, turpis eget laoreet  varius, lorem sem volutpat diam, non feugiat lorem tellus mollis mauris.  Nullam id tellus enim.</p>',
  'title': u'aaaaa'},
 'IRelated_1': {},
 'IRelated_10': {},
 'IRelated_11': {},
 'IRelated_12': {},
 'IRelated_13': {},
 'IRelated_14': {},
 'IRelated_15': {},
 'IRelated_2': {},
 'IRelated_3': {},
 'IRelated_4': {},
 'IRelated_5': {},
 'IRelated_6': {},
 'IRelated_7': {},
 'IRelated_8': {},
 'IRelated_9': {},
 'ISimpleBox_1': {'subtitle': u'sub',
  'target': '/news/nova-noticia',
  'text': u'<p>\xc9 muito <b>legal</b>! mesmo.</p>\r\n<p>\xa0</p>\r\n<p><b>Editando e tudo!</b></p>',
  'title': u'Tit'},
 'ISimpleBox_2': {},
 'ISimpleBox_3': {},
 'ISuperTitleBox_0': {'image': u'/++theme++il.portalinterlegis/temp/images/interlegis.jpg',
  'supertitle': u'Super T\xedtulo',
  'target': '/news/nova-noticia',
  'text': u'<p>Donec dui diam, bibendum eu tincidunt a, vehicula ac sem. Sed placerat diam in magna placerat ultrices. Donec in posuere est. Curabitur dictum pulvinar risus, id laoreet enim pretium eu.</p>',
  'title': u'T\xedtulo <b>legal</b>'},
 'ISuperTitleBox_1': {},
 'ISuperTitleBox_2': {},
 'ISuperTitleBox_3': {},
 'ITabsPilares_1': {},
 'carousel_panels_carousel_0': [0, 1, 2],
 'carousel_panels_products-and-services_0': [3, 4]}
