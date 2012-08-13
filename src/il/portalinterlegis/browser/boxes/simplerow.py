# -*- coding: utf-8 -*-
from manager import get_template, Row

class SimpleRow(Row):

    def __init__(self, title, *row_spec):
        self.title = title
        self.row_spec = row_spec
        super(SimpleRow, self).__init__(*row_spec)

    def __call__(self, context):
        template = get_template('simplerow.html')
        return template.render(
            title=self.title,
            cells=self.cells(context))
