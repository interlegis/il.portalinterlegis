# -*- coding: utf-8 -*-
from five import grok
from persistent.dict import PersistentDict
from plone.app.event.recurrence import RecurrenceSupport
from plone.autoform.form import AutoExtensibleForm
from plone.directives.form import Schema
from plone.event.interfaces import IOccurrence
from z3c.form.form import EditForm
from zope import schema
from zope.annotation import IAnnotations


def get_or_create(dictionary, key):
    if key not in dictionary:
        dictionary[key] = PersistentDict()
    return dictionary[key]

def get_occurrence_adjustments(event):
    annotations = IAnnotations(event)
    return get_or_create(annotations, 'event_occurrence_adjustments')

class InterlegisRecurrenceSupport(RecurrenceSupport):

    def occurrences(self, range_start=None, range_end=None):
        adjustments = get_occurrence_adjustments(self.context)

        def adjust_occurrence(occ):
            if IOccurrence.providedBy(occ):
                occ.original_values = (occ.start, occ.end)
                adj = adjustments.get(occ.id)
                if adj:
                    occ.start = adj.get('start', occ.start)
                    occ.end = adj.get('end', occ.end)
            return occ

        originals = super(InterlegisRecurrenceSupport, self).occurrences(range_start, range_end)
        return map(adjust_occurrence, originals)


class IOccurrenceAdjustment(Schema):
    start = schema.Datetime(title=u"Inicio")
    end = schema.Datetime(title=u"Fim")

class OccurrenceAdjustment(grok.Adapter):
    grok.provides(IOccurrenceAdjustment)
    grok.context(IOccurrence)

    @property
    def start(self):
        return self.context.start

    @start.setter
    def start(self, value):
        self.context.start = value

    @property
    def end(self):
        return self.context.end

    @end.setter
    def end(self, value):
        self.context.end = value

def save_adjustment(occ):
    event = occ.getParentNode()
    adjustments = get_occurrence_adjustments(event)

    now = (occ.start, occ.end)
    occ_adjustment = get_or_create(adjustments, occ.id)
    if now == occ.original_values:
        del adjustments[occ.id]
    else:
        occ_adjustment.clear()
        for key, n, o in zip(['start', 'end'], now, occ.original_values):
            if n != o:
                occ_adjustment[key] = n

class OccurrenceAdjustmentView(AutoExtensibleForm, EditForm, grok.View):
    grok.context(IOccurrence)
    grok.name('adjust')
    grok.require('cmf.ModifyPortalContent')
    schema = IOccurrenceAdjustment

    def applyChanges(self, data):
        # add missing timezone info to data
        data['start'] = data['start'].replace(tzinfo=self.context.start.tzinfo)
        data['end'] = data['end'].replace(tzinfo=self.context.end.tzinfo)
        changes = super(OccurrenceAdjustmentView, self).applyChanges(data)
        save_adjustment(self.context)
        return changes
