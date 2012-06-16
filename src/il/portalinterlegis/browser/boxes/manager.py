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

template_factory = Environment(loader=PackageLoader(__name__))

class EditableBox(object):

    TEMPLATE_NAME = 'editablebox.html'

    def __init__(self, permission=ModifyPortalContent):
        self.permission = permission

    def __call__(self, context):
        editablebox_template = template_factory.get_template(self.TEMPLATE_NAME)
        return editablebox_template.render(
            box = self,
            is_editable = self.is_editable(context),
            inner = self.inner_render(context))

    def is_editable(self, context):
        return getSecurityManager().checkPermission(self.permission, context)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def edit_href(self):
        raise NotImplementedError

    def inner_render(self, context):
        raise NotImplementedError


class Box(EditableBox):

    ALL_BOXES_KEY = 'il.portalinterlegis.boxes'

    def __init__(self, schema, number, permission=ModifyPortalContent, form_label=None):
        super(Box, self).__init__(permission)
        self.schema = schema
        self.number = number
        self.form_label = form_label or u'Edite os valore desta caixa' #TODO: improve this text

    @property
    def id(self):
        return '%s_%s' % (self.schema.__name__, self.number)

    def inner_render(self, context):
        template = template_factory.get_template(self.schema.__name__.lower() + '.html')
        return template.render(self.content(context))

    def content(self, context):
        annotations = IAnnotations(context)
        boxes = get_or_create_persistent_dict(annotations, self.ALL_BOXES_KEY)
        return get_or_create_persistent_dict(boxes, self.id)

    @property
    def form_name(self):
        """Last part of form urls.
        """
        return 'box_%s' % self.id

    edit_href = form_name # To be overridden independently


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
            return box.content(self.context)

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

def build_many_box_forms(schema, max_number):
    for number in range(1, max_number+1):
        build_box_form(Box(schema, number))

def get_or_create_persistent_dict(dictionary, key):
    value = dictionary.get(key, None)
    if not value:
        dictionary[key] = value = PersistentDict()
    return value

# ROWS
class DtRow(object):

    ROW_TEMPLATE = '''
  <div class="dt-row">%s
  </div>'''

    CELL_TEMPLATE = '''
    <div class="dt-cell dt-position-%s dt-width-%s">%s
    </div>'''

    def __init__(self, *row_spec):
        try:
            for (width, template) in row_spec: pass
        except ValueError, e:
            e.args += row_spec
            raise
        self.row_spec = row_spec

    def _cells(self, context):
        """Iterates transforming each cell spec from (width, template) to
           (position, width, rendered_html)
        """
        position = 0
        for (width, template) in self.row_spec:
            yield (position, width, template(context))
            position += width

    def render(self, context):
        """Renders the html of one row.
        `row_spec` is a sequence of cell specs: [(width, schema, number), ...]
        """
        return self.ROW_TEMPLATE % ''.join(
            [self.CELL_TEMPLATE % cell for cell in self._cells(context)])


class GridView(grok.View):
    "Base class for all grid-like views"
    martian.baseclass()

    template = ZopeTwoPageTemplate(filename="gridview.pt")

    def rows(self):
        for row in self.grid:
            yield row.render(self.context)

################################################################
# TODO: o unico lugar em que isto funcionou foi aqui. Entender porque e decidir lugar definitivo.

# initialize all the box managers
for s in box_schemas():
    build_many_box_forms(s, 10)

