# -*- coding: utf-8 -*-
import sys
import inspect

from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform.interfaces import WIDGETS_KEY
from plone.directives import form
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import PathSourceBinder
from zope import schema


class BoxSchema(form.Schema):
    """Marker interface for box schemas.
    """


# decorator
def rich(**kwargs):
    def f(cls):
        cls.setTaggedValue(WIDGETS_KEY, dict(**kwargs))
        return cls
    return f


# TODO: title in "almost" WysiwygFieldWidget... (just <b></b> allowed)... configure Tiny and filters
@rich(text=WysiwygFieldWidget, target=AutocompleteFieldWidget)
class IRelated(BoxSchema):
    target = schema.Choice(title=u"Conteúdo relacionado",
                           source=PathSourceBinder(),
                           required=False)
    image = schema.TextLine(title=u"URL da imagem", required=False)  # TODO: localizar ou subir imagem
    title = schema.TextLine(title=u"Título", required=True)
    text = schema.Text(title=u"Texto", required=False)


class ISuperTitleBox(IRelated):
    # TODO: usar hint para que este campo seja o primeiro
    supertitle = schema.TextLine(title=u"Supertítulo", required=True)


class ICarouselItem(IRelated):
    # It's important to have a separate class (instead of using IRelated directly)
    # since the class name is used for storage
    pass


class ICalendar(BoxSchema):
    pass


class IAcompanheOInterlegis(BoxSchema):
    pass


class IHighlight(BoxSchema):
    pass


def box_schemas():
    """Returns all the BoxSchema's in this module.
    """
    return [cls for name, cls in inspect.getmembers(sys.modules[__name__])
            if hasattr(cls, 'extends') and cls.extends(BoxSchema)]
