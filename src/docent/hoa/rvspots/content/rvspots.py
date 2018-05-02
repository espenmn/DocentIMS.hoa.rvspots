# -*- coding: utf-8 -*-
from plone import api
from plone.app.textfield import RichText
from plone.dexterity.content import Item, Container
from plone.dexterity.utils import createContent
from plone.directives import form
from plone.namedfile.field import NamedBlobImage

from docent.hoa.rvspots.app_config import RV_MANAGERS_GID

import logging
logger = logging.getLogger("Plone")

from docent.hoa.rvspots import _



class IRVSpots(form.Schema):
    """
    Uses IDublinCore
    """
    spot_map = NamedBlobImage(title=_(u"RV Spot Map"),
                              description=_(u"Please upload an image of the spot map."),
                              required=False)

    body = RichText(
        title=u"RV Spots Text",
        required=False
    )

class RVSpots(Container):
    """
    """

    def after_creation_processor(self, event):
        self.manage_setLocalRoles(RV_MANAGERS_GID, ['Editor'])

        id_iter = 1
        for i in range(19):
            spot_id = 'spot_%s' % id_iter
            if spot_id in self.objectIds():
                api.portal.show_message(message="Spot Id: %s already exists." % spot_id,
                                        request=self.REQUEST,
                                        type='info')
            else:
                spot_obj = createContent('docent.hoa.rvspot',
                                         id=spot_id.encode('ascii', 'ignore'),
                                         title=u"Spot %s" % id_iter)
                self._setObject(spot_id.encode('ascii', 'ignore'), spot_obj)
                setattr(spot_obj, 'spot_id', id_iter)

            id_iter += 1