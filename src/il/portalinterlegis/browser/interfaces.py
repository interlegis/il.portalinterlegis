# -*- coding: utf-8 -*-
from zope.interface import Interface


class IThemeSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "il.portalinterlegis" theme,
       this interface must be its layer.
    """

# HOMES


class IComunidadeLegislativa(Interface):
    "Marker interface para home"


class IInformacao(Interface):
    "Marker interface para home"


class ICapacitacao(Interface):
    "Marker interface para home"


class ITecnologia(Interface):
    "Marker interface para home"


class IComunicacao(Interface):
    "Marker interface para home"
