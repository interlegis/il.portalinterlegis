# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import ModifyPortalContent
from five import grok
from five.grok.components import ZopeTwoPageTemplate
from persistent.list import PersistentList
from zope.interface import Interface

from interfaces import ICarouselItem
from manager import BoxAware, Box, NUMBER_OF_PRE_CREATED_BOXES, get_template, BaseBox


class Carousel(BoxAware):
    """General carousel manager, related to a context"""

    def __init__(self, number, context):
        self.number = number
        self.context = context

    def render(self, edit_mode=False):
        if edit_mode:
            template = get_template("carousel-edit.html")
        else:
            template = get_template("carousel.html")
        boxes = [(number, Box(ICarouselItem, number)) for number in self.numbers]
        return template.render(
            carousel_edit_href=carousel_edit_href(self.number),
            items=[(number,
                    box.get_data(self.context),
                    box.edit_href) for number, box in boxes])

    # TODO: renomear isso para panels
    @property
    def numbers(self):
        return self.get_box_data(self.context,
                                 "carousel_numbers_%s" % self.number,
                                 PersistentList)

    def add_item(self):
        numbers = self.numbers
        for i in range(NUMBER_OF_PRE_CREATED_BOXES):
            if i not in numbers and Box(ICarouselItem, number).is_empty(self.context):
                numbers.insert(0, i)
                break

    def remove_item(self, id):
        index = self._index_from_id(id)
        self.numbers.remove(index)
        Box(ICarouselItem, index).erase_data(self.context)

    def reorder(self, ids):
        self.numbers[:] = [self._index_from_id(id) for id in ids.split(',')]

    def _index_from_id(self, id):
        return int(id.split('_')[-1])


class CarouselBox(BaseBox):

    id = 'carousel'
    is_link_overlay = False

    def __init__(self, number, permission=ModifyPortalContent):
        super(CarouselBox, self).__init__(permission)
        self.number = number

    def inner_render(self, context):
        return Carousel(self.number, context).render()

    @property
    def edit_href(self):
        return carousel_edit_href(self.number)


def carousel_edit_href(number):
    return "carousel_edit_%s" % number

def build_CarouselEditView(number):

    class CarouselEditView(grok.View):
        grok.name(carousel_edit_href(number))
        grok.context(Interface)
        grok.require('cmf.ModifyPortalContent')

        template = ZopeTwoPageTemplate(filename="carouseledit.pt")
        number = number

        def carousel(self):
            return self._carousel.render(edit_mode=True)

        def update(self, **kwargs):
            self._carousel = Carousel(self.number, self.context)
            if 'add' in self.request:
                self._carousel.add_item()
            elif 'remove' in self.request:
                self._carousel.remove_item(self.request['remove'])
            elif 'reorder' in self.request:
                self._carousel.reorder(self.request['reorder'])

    globals()['CarouselEditView_%s' % number] = CarouselEditView

# XXX: one more elaborated POG, to avoid complex traversals
for number in range(8):
    build_CarouselEditView(number)

