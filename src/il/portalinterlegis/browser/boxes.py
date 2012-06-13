import martian
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import IFolderish
from five import grok
from five.grok.components import ZopeTwoPageTemplate
from persistent.dict import PersistentDict
from plone.autoform.form import AutoExtensibleForm
from z3c.form import form, datamanager
from z3c.form.interfaces import IDataManager
from zope.annotation import IAnnotations
from zope.component import adapts, provideAdapter
from zope.interface import implements
from zope.schema.interfaces import IField

from interfaces import template_dict, box_schemas


class PersistentDictionaryField(datamanager.DictionaryField):
    adapts(PersistentDict, IField)
    implements(IDataManager)
provideAdapter(PersistentDictionaryField)


class BoxManager(object):

    ALL_BOXES_KEY = 'il.portalinterlegis.boxes'

    def __init__(self, schema, label=None):
        self.schema = schema
        #TODO: improve this text
        self.form_label = label or u'Edite os valore desta caixa'

    def build_form(self, number):

        # the combination (form.EditForm, grok.View)
        # is from https://mail.zope.org/pipermail/grok-dev/2008-July/005999.html
        # (plone.directives.form.EditForm did not work well)
        class BoxEditForm(AutoExtensibleForm, form.EditForm, grok.View):
            grok.context(IFolderish)
            grok.name(self._box_name_for_url(number))
            grok.require('cmf.ModifyPortalContent')

            label = self.form_label
            schema = self.schema

            def getContent(form_self):
                return self.box_content(form_self.context, number)

            def render(self):
                # we cannot simply associtate this template in the class level
                # because form.EditForm has a ".render()" method and grok.View
                # assumes you cannot have both "template = ..." and ".render()".
                # No problem, we make a method that simply renders the template
                template = ZopeTwoPageTemplate(filename="boxform.pt")
                return template.render(self)

        globals()['BoxEditForm_%s' % self._box_key(number)] = BoxEditForm
        return BoxEditForm

    def build_n_forms(self, max_number):
        for number in range(1, max_number+1):
            self.build_form(number)

    def box_content(self, context, number): # maybe this method should be private
        annotations = IAnnotations(context)
        boxes = get_or_create_persistent_dict(annotations, BoxManager.ALL_BOXES_KEY)
        return get_or_create_persistent_dict(boxes, self._box_key(number))

    def html(self, context, number):
        return self._schema_template() % NiceDictGetter(
            self.box_content(context, number))

    def _box_key(self, number):
        return '%s_%s' % (self.schema.__name__, number)

    def _box_name_for_url(self, number):
        return 'box_%s' % self._box_key(number)

    def _schema_template(self):
        return template_dict[self.schema]

def get_or_create_persistent_dict(dictionary, key):
    value = dictionary.get(key, None)
    if not value:
        dictionary[key] = value = PersistentDict()
    return value

class NiceDictGetter(object):
    """Dictionary getter with a default empty string for unknown keys.
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getitem__(self, key):
        value = self.wrapped.get(key, None)
        return (value is None) and '---' or value

# ROWS

ROW_TEMPLATE = '''
  <div class="dt-row">%s
  </div>'''

CELL_TEMPLATE = '''
    <div id="%s" class="%s dt-cell dt-position-%s dt-width-%s">%s
    </div>'''

# TODO: refactor these functions to live inside GridView @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def row_spec_to_cells(context, row_spec):
    """Iterates transforming each cell spec from
       (width, schema, number) to
       (id, additional_classes, position, width, html)
    """
    position = 0
    for (width, schema, number) in row_spec:
        boxmanager = BoxManager(schema)
        if getSecurityManager().checkPermission(permissions.ModifyPortalContent, context):
            additional_classes = 'editable-box'
        else:
            additional_classes = ''
        yield (boxmanager._box_key(number),
               additional_classes,
               position,
               width,
               boxmanager.html(context, number))
        position += width

def row_html(context, row_spec):
    """Renders the html of one row.
    `row_spec` is a sequence of cell specs: [(width, schema, number), ...]
    """
    return ROW_TEMPLATE % ''.join(
        [CELL_TEMPLATE % cell for cell in row_spec_to_cells(context, row_spec)])

class GridView(grok.View):
    "Base class for all grid-like views"
    martian.baseclass()

    template = ZopeTwoPageTemplate(filename="gridview.pt")

    def rows(self):
        for row_spec in self.grid:
            yield row_html(self.context, row_spec)

################################################################
# TODO: o unico lugar em que isto funcionou foi aqui. Entender porque e decidir lugar definitivo.

# initialize all the box managers

for s in box_schemas():
    BoxManager(s).build_n_forms(10)

