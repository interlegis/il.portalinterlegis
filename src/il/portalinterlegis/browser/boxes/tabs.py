# -*- coding: utf-8 -*-
from manager import get_template, Row

from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


class Tab(Row):

    template_name = 'tab.html'

    def __init__(self, title, inner_title, *row_spec):
        self.title = title
        self.inner_title = inner_title
        self.row_spec = row_spec
        super(Tab, self).__init__(*row_spec)

    def __call__(self, context):
        return self.render(context)

    def __repr__(self):
        util = queryUtility(IIDNormalizer)
        return 'tab-%s' % util.normalize(self.title)

    def render(self, context):
        return get_template(self.template_name).render(
            cells=self.cells(context),
            title=self.title,
            inner_title=self.inner_title)


class TabbedPane(object):

    def __init__(self, *tabs):
        self.tabs = tabs

    def __call__(self, context):
        template = get_template('tabbedpane.html')
        return template.render(
            slug_title=[(tab, tab.title) for tab in self.tabs],
            tabs=[tab(context) for tab in self.tabs])
