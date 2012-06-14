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

templates = Environment(loader=PackageLoader(__name__))

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
        template = templates.get_template(self.schema.__name__.lower() + '.html')
        return template.render(self.box_content(context, number))

    def _box_key(self, number):
        return '%s_%s' % (self.schema.__name__, number)

    def _box_name_for_url(self, number):
        return 'box_%s' % self._box_key(number)


def get_or_create_persistent_dict(dictionary, key):
    value = dictionary.get(key, None)
    if not value:
        dictionary[key] = value = PersistentDict()
    return value
from exceptions import ValueError
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


class Box(object):

    BOX_TEMPLATE = '''
      <div id="%s"%s>%s
      </div>'''

    def __init__(self, schema, number, permission=ModifyPortalContent):
        self.schema = schema
        self.number = number
        self.permission = permission

    def __call__(self, context):
        boxmanager = BoxManager(self.schema)
        is_editable = getSecurityManager().checkPermission(self.permission, context)
        return self.BOX_TEMPLATE % (boxmanager._box_key(self.number),
                                    ' class ="editable-box"' if is_editable else '',
                                    boxmanager.html(context, self.number))


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
    BoxManager(s).build_n_forms(10)

