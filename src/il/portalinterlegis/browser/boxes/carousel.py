# -*- coding: utf-8 -*-
from five import grok
from five.grok.components import ZopeTwoPageTemplate
from persistent.list import PersistentList
from zope.interface import Interface

from interfaces import ICarouselItem
from manager import BoxAware, Box, NUMBER_OF_PRE_CREATED_BOXES, get_template, BaseBox


class Carousel(BoxAware):
    """General carousel manager, related to a context"""

    CAROUSEL_KEY = "carousel"
    NUMBERS_KEY = "numbers"

    def __init__(self, context):
        self.context = context

    def render(self, edit_mode=False):
        if edit_mode:
            template = get_template("carousel-edit.html")
        else:
            template = get_template("carousel.html")
        boxes = [(number, Box(ICarouselItem, number)) for number in self.numbers]
        return template.render(
            items=[(number,
                    box.get_data(self.context),
                    box.edit_href) for number, box in boxes])

    @property
    def numbers(self):
        data = self.get_box_data(self.context, self.CAROUSEL_KEY)
        return self.get_or_create_from_dict(data, self.NUMBERS_KEY, PersistentList)

    def add_item(self):
        numbers = self.numbers
        for i in range(NUMBER_OF_PRE_CREATED_BOXES):
            if i not in numbers:
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


class CarouselEditView(grok.View):

    EDIT_CAROUSEL = 'edit-carousel'

    grok.name(EDIT_CAROUSEL)
    grok.context(Interface)
    grok.require('cmf.ModifyPortalContent')

    template = ZopeTwoPageTemplate(filename="carouseledit.pt")

    def carousel(self):
        return self._carousel.render(edit_mode=True)

    def update(self, **kwargs):
        self._carousel = Carousel(self.context)
        if 'add' in self.request:
            self._carousel.add_item()
        elif 'remove' in self.request:
            self._carousel.remove_item(self.request['remove'])
        elif 'reorder' in self.request:
            self._carousel.reorder(self.request['reorder'])
    # TODO: ajustar o render para retornar apenas feedback de sucesso ou falha

class CarouselBox(BaseBox):

    id = 'carousel'
    edit_href = CarouselEditView.EDIT_CAROUSEL
    is_link_overlay = False

    def inner_render(self, context):
        return Carousel(context).render()
