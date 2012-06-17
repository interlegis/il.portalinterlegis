# -*- coding: utf-8 -*-
import sys, inspect

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
def rich(*args, **kwargs):
    def f(cls):
        cls.setTaggedValue(WIDGETS_KEY,
                           dict([(k, WysiwygFieldWidget) for k in args],
                                **kwargs))
        return cls
    return f


@rich('text', target=AutocompleteFieldWidget)
class ISimpleBox(BoxSchema):
    title = schema.TextLine(title=u"Título", required=True)
    subtitle = schema.TextLine(title=u"Subtítulo", required=True)
    text = schema.Text(title=u"Texto", required=False)
    target = schema.Choice(title=u"Conteúdo relacionado",
                            source=PathSourceBinder(),
                            required=False)


@rich('text', target=AutocompleteFieldWidget)
class ICarousel(BoxSchema):
    title = schema.TextLine(title=u"Título", required=True)
    text = schema.Text(title=u"Texto", required=False)
    target = schema.Choice(title=u"Conteúdo relacionado",
                           source=PathSourceBinder(portal_type='Document'))


class ICalendar(BoxSchema):
    pass


class IAcompanheOInterlegis(BoxSchema):
    pass


class ITabsPilares(BoxSchema):
    pass


class IHighlight(BoxSchema):
    pass


def box_schemas():
    """Returns all the BoxSchema's in this module.
    """
    return [cls for name, cls in inspect.getmembers(sys.modules[__name__])
            if hasattr(cls, 'extends') and cls.extends(BoxSchema)]
