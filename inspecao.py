# -*- coding: utf-8 -*-

# Este arquivo contém trechos de código que podem ser usados para inspeção rápida no prompt

from zope.annotation import IAnnotations
aa = IAnnotations(context)['il.portalinterlegis.boxes']
aa['ISimpleBox_1']

from il.portalinterlegis.browser.boxes import BoxManager
from il.portalinterlegis.browser.interfaces import ISimpleBox
boxmanager = BoxManager(ISimpleBox)
boxmanager.box_content(context, 1)

from Testing.ZopeTestCase.utils import startZServer
startZServer()

with open("out", "w+") as f: f.write(browser.contents)
