# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import ModifyPortalContent
from five import grok
from five.grok.components import ZopeTwoPageTemplate
from persistent.list import PersistentList
from zope.interface import Interface

from interfaces import ICarouselItem
from manager import BoxAware, Box, NUMBER_OF_PRE_CREATED_BOXES, get_template, BaseBox


class Carousel(BoxAware):
    """General carousel manager, related to a context
    """

    def __init__(self, kind, number, context):
        self.kind = kind
        self.number = number
        self.context = context

    def render(self, edit_mode=False):
        if edit_mode:
            template = get_template("%s-edit.html" % self.kind)
        else:
            template = get_template("%s.html" % self.kind)
        boxes = [(panel, Box(ICarouselItem, panel)) for panel in self.panels]
        return template.render(
            carousel_edit_href=carousel_edit_href(self.kind, self.number),
            items=[(panel,
                    box.get_data(self.context),
                    box.edit_href) for panel, box in boxes])

    @property
    def panels(self):
        return self.get_box_data(self.context, self._panels_key(), PersistentList)

    def _panels_key(self):
        return "carousel_panels_%s_%s" % (self.kind, self.number)

    def add_item(self):
        panels = self.panels
        for i in range(NUMBER_OF_PRE_CREATED_BOXES):
            if i not in panels and Box(ICarouselItem, i).is_empty(self.context):
                panels.insert(0, i)
                # this marks the slot as used
                # to avoid conflicts between panels of two carousels
                Box(ICarouselItem, i).get_data(self.context)
                break

    def remove_item(self, id):
        index = self._index_from_id(id)
        self.panels.remove(index)
        Box(ICarouselItem, index).erase_data(self.context)

    def reorder(self, ids):
        self.panels[:] = [self._index_from_id(id) for id in ids.split(',')]

    def _index_from_id(self, id):
        return int(id.split('_')[-1])


class CarouselBox(BaseBox):

    is_link_overlay = False
    kind = 'carousel'

    def __init__(self, number, permission=ModifyPortalContent):
        super(CarouselBox, self).__init__(permission)
        self.number = number

    @property
    def id(self):
        return '%s_%s' % (self.kind, self.number)

    def inner_render(self, context):
        return Carousel(self.kind, self.number, context).render()

    @property
    def edit_href(self):
        return carousel_edit_href(self.kind, self.number)


def carousel_edit_href(kind, number):
    return "carousel_edit_%s_%s" % (kind, number)


def build_CarouselEditView(kind, number):

    class CarouselEditView(grok.View):
        grok.name(carousel_edit_href(kind, number))
        grok.context(Interface)
        grok.require('cmf.ModifyPortalContent')

        template = ZopeTwoPageTemplate(filename="carouseledit.pt")
        kind = kind
        number = number

        def carousel(self):
            return self._carousel.render(edit_mode=True)

        def update(self, **kwargs):
            self._carousel = Carousel(self.kind, self.number, self.context)
            if 'add' in self.request:
                self._carousel.add_item()
            elif 'remove' in self.request:
                self._carousel.remove_item(self.request['remove'])
            elif 'reorder' in self.request:
                self._carousel.reorder(self.request['reorder'])

    globals()['CarouselEditView_%s_%s' % (kind, number)] = CarouselEditView


class ProductsAndServices(CarouselBox):
    kind = 'products-and-services'

# XXX: one more elaborated POG, to avoid complex traversals
for kind in CarouselBox.kind, ProductsAndServices.kind:
    for number in range(8):
        build_CarouselEditView(kind, number)
