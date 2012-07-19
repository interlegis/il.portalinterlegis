import martian
from AccessControl import getSecurityManager
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.permissions import ModifyPortalContent
from five import grok
from five.grok.components import ZopeTwoPageTemplate
from jinja2 import Environment, PackageLoader
from persistent.dict import PersistentDict
from plone.autoform.form import AutoExtensibleForm
from z3c.form import form, datamanager
from z3c.form.interfaces import IDataManager
from zope.annotation import IAnnotations
from zope.component import adapts, provideAdapter
from zope.interface import implements
from zope.schema.interfaces import IField

from interfaces import box_schemas


class PersistentDictionaryField(datamanager.DictionaryField):
    adapts(PersistentDict, IField)
    implements(IDataManager)
provideAdapter(PersistentDictionaryField)

_template_factory = Environment(loader=PackageLoader(__name__))

get_template = _template_factory.get_template


class BoxAware(object):

    ALL_BOXES_KEY = 'il.portalinterlegis.boxes'

    def has_box_data(self, context, key):
        annotations = IAnnotations(context)
        return self.ALL_BOXES_KEY in annotations \
          and key in annotations[self.ALL_BOXES_KEY]

    def get_box_data(self, context, key, type_to_create=PersistentDict):
        annotations = IAnnotations(context)
        boxes = self.get_or_create_from_dict(annotations, self.ALL_BOXES_KEY)
        return self.get_or_create_from_dict(boxes, key, type_to_create)

    def erase_box_data(self, context, key):
        annotations = IAnnotations(context)
        boxes = annotations.get(self.ALL_BOXES_KEY, None)
        if boxes and key in boxes:
            del boxes[key]

    @classmethod
    def get_or_create_from_dict(cls, dictionary, key, type_to_create=PersistentDict):
        value = dictionary.get(key, None)
        if not value:
            dictionary[key] = value = type_to_create()
        return value


class BaseBox(BoxAware):
    """Base abstract class for editable boxes.
    """

    is_link_overlay = True

    def __init__(self, permission=ModifyPortalContent):
        self.permission = permission

    def __call__(self, context):
        return get_template('basebox.html').render(
            box=self,
            has_permission=self.has_permission(context),
            inner=self.inner_render(context))

    def has_permission(self, context):
        return getSecurityManager().checkPermission(self.permission, context)

    @property
    def id(self):
        "id of the box. Used in the template. Must be unique on a page."
        raise NotImplementedError

    @property
    def edit_href(self):
        raise NotImplementedError

    def inner_render(self, context):
        raise NotImplementedError


class Box(BaseBox):

    def __init__(self, schema, number, permission=ModifyPortalContent, form_label=None):
        super(Box, self).__init__(permission)
        self.schema = schema
        self.number = number
        self.form_label = form_label or u'Edite esta caixa'  # TODO: improve this text

    @property
    def id(self):
        return '%s_%s' % (self.schema.__name__, self.number)

    def inner_render(self, context):
        templ = get_template(self.schema.__name__.lower() + '.html')
        return templ.render(self.get_data(context))

    def get_data(self, context):
        return self.get_box_data(context, self.id)

    def erase_data(self, context):
        self.erase_box_data(context, self.id)

    def is_empty(self, context):
        return not self.has_box_data(context, self.id)

    @property
    def form_name(self):
        """Last part of form urls.
        """
        return 'box_%s' % self.id

    edit_href = form_name  # To be overridden independently


def build_box_form(box):

    # the combination (form.EditForm, grok.View)
    # is from https://mail.zope.org/pipermail/grok-dev/2008-July/005999.html
    # (plone.directives.form.EditForm did not work well)
    class BoxEditForm(AutoExtensibleForm, form.EditForm, grok.View):
        grok.context(IFolderish)
        grok.name(box.form_name)
        grok.require('cmf.ModifyPortalContent')

        label = box.form_label
        schema = box.schema

        def getContent(self):
            return box.get_data(self.context)

        def render(self):
            # we cannot simply associtate this template in the class level
            # because form.EditForm has a ".render()" method and grok.View
            # assumes you cannot have both "template = ..." and ".render()".
            # No problem, we make a method that simply renders the template

            # hack to make forms appear in ajax mode even using an iframe
            # setting ajax_load is useless, probably because of a bug in plone
            # TODO: check later if there is a more natural way of doing this
            self.request['disable_plone.leftcolumn'] = True
            self.request['disable_plone.rightcolumn'] = True
            template = ZopeTwoPageTemplate(filename="boxform.pt")
            return template.render(self)

    globals()['BoxEditForm_%s' % box.id] = BoxEditForm
    return BoxEditForm


# TODO: This is first class POG. Has to be eliminated someday
def build_many_box_forms(schema, max_number):
    for number in range(max_number):
        build_box_form(Box(schema, number))


def get_or_create_persistent_dict(dictionary, key):
    value = dictionary.get(key, None)
    if not value:
        dictionary[key] = value = PersistentDict()
    return value


# ROWS
class Row(object):
    """Abstract class for rows. Subclasses must define 'template_name'
    """

    def __init__(self, *row_spec):
        try:
            for (width, renderable) in row_spec:
                pass
        except ValueError, e:
            e.args += row_spec
            raise
        self.row_spec = row_spec

    def cells(self, context):
        """Iterates transforming each cell spec from (width, renderable) to
           a dict of {position, width, rendered_html}
        """
        position = 0
        for (width, renderable) in self.row_spec:
            yield dict(position=position, width=width, html=renderable(context))
            position += width

    def render(self, context):
        """Renders the html of one row.
        `row_spec` is a sequence of cell specs: [(width, schema, number), ...]
        """
        return get_template(self.template_name).render(cells=self.cells(context))


class DtRow(Row):

    template_name = 'dtrow.html'


class GridView(grok.View):
    "Base class for all grid-like views"
    martian.baseclass()

    template = ZopeTwoPageTemplate(filename="gridview.pt")

    def rows(self):
        for row in self.grid:
            yield row.render(self.context)

################################################################
# TODO: o unico lugar em que isto funcionou foi aqui. Entender por que e decidir lugar definitivo.

# initialize all the box managers
NUMBER_OF_PRE_CREATED_BOXES = 20
for s in box_schemas():
    build_many_box_forms(s, NUMBER_OF_PRE_CREATED_BOXES)
