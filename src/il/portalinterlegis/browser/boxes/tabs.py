# -*- coding: utf-8 -*-
from manager import get_template


class Tab(object):

    def __init__(self, title, inner_title, *row_spec):
        self.title = title
        self.inner_title = inner_title
        self.row_spec = row_spec

    def __call__(self, context):
        return 'TODO: TAB %s' % self.title


class TabbedPane(object):

    def __init__(self, *tabs):
        self.tabs = tabs

    def __call__(self, context):
        template = get_template("tabbedpane.html")
        return template.render(
            tabs=[(tab.title, tab(context)) for tab in self.tabs])
