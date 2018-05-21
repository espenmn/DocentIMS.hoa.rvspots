# -*- coding: utf-8 -*-
from Products.Five import BrowserView


import logging
logger = logging.getLogger("Plone")


class RVSpotView(BrowserView):

    def __call__(self):
        context = self.context
        parent = context.aq_parent
        return self.request.response.redirect(parent.absolute_url())

