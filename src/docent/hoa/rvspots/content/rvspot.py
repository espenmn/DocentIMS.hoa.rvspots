# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.content import Item, Container
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

import logging
logger = logging.getLogger("Plone")

from docent.hoa.rvspots import _

def spotCostVocabulary():
    terms = []
    for i in range(25,80,5):
        terms.append(SimpleVocabulary.createTerm(str(i), str(i), u"$%s" % i))
    return SimpleVocabulary(terms)

class IRVSpot(form.Schema):
    """
    Uses IDublinCore
    """

    form.mode(spot_id='display')
    spot_id = schema.Int(title=_(u"Spot Id"),
                         description=_(u""),
                         required=False,
                         default=0,)

    spot_size = schema.TextLine(title=_(u"Size"),
                                description=_(u"RV Spot Dimensions"),
                                required=False)

    spot_cost = schema.Choice(title=_(u"Cost"),
                              description=_(u"How much to rent this spot?"),
                              vocabulary=spotCostVocabulary(),
                              required=False)

    homeowner = schema.Choice(title=_(u"Homeowner"),
                              description=_(u"Select the homeowner that is renting this spot."),
                              vocabulary="docent.hoa.rvspots.homeowners",
                              required=False)

    homeowner_contract = NamedBlobFile(title=_(u"Owner Contract"),
                                        description=_(u"Upload the owner's contract here."),
                                        required=False)

    renter = schema.Choice(title=_(u"Renter"),
                           description=_(u"Select the renter that will use this spot."),
                           vocabulary="docent.hoa.rvspots.rentersandowners",
                           required=False)

    renter_contract = NamedBlobFile(title=_(u"Renter Contract"),
                                    description=_(u"Upload the renter's contract here."),
                                    required=False)

    key_number = schema.TextLine(title=_(u"Key Number"),
                                 required=False)

    occupancy = schema.Datetime(title=_(u"Occupancy Date"),
                                description=_(u"Start date of occupancy."),
                                required=False)

    insurance_file = NamedBlobFile(title=_(u"Insurance File"),
                                        description=_(u"Upload the insurance file."),
                                        required=False)

class RVSpot(Item):
    """
    """
