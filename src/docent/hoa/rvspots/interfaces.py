# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from docent.hoa.rvspots import _
from plone.directives import form
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocentHoaRvspotsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IStoreVocabularyData(form.Schema):

    home_owners_tuples_json = schema.TextLine(
        title=_(u"Home Owners JSON"),
        description=_(u"Computed Field."),
        required=False,
        )

    renters_tuples_json = schema.TextLine(
        title=_(u"Renters JSON"),
        description=_(u"Computed Field"),
        required=False,
        )

    home_owners_last_build_date = schema.ASCIILine(
        title=_(u"Home Owners Last Build Date"),
        description=_(u"Computed Field."),
        required=False,
        )

    renter_last_build_date = schema.ASCIILine(
        title=_(u"Renters Last Build Date"),
        description=_(u"Computed Field."),
        required=False,
        )
