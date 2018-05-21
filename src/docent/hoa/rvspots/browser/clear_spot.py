# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter

import logging
logger = logging.getLogger("Plone")

class ClearSpotView(BrowserView):
    def __call__(self):
        authenticator=getMultiAdapter((self.context, self.request), name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized
        return self.render()

    def render(self):
        context = self.context

        setattr(context, 'homeowner', '')
        setattr(context, 'renter', '')
        setattr(context, 'homeowner_contract', None)
        setattr(context, 'renter_contract', None)
        setattr(context, 'occupancy', None)
        setattr(context, 'key_number', u'')
        setattr(context, 'insurance_file', None)

        parent = context.aq_parent
        return self.request.response.redirect(parent.absolute_url())

