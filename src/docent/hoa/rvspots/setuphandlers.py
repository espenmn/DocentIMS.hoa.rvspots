# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from docent.hoa.rvspots.app_config import RV_MANAGERS_GID, HOMEOWNER_AND_RENTER_GID, HOME_OWNERS_GID, RENTERS_GID

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'docent.hoa.rvspots:uninstall',
        ]

def createGroupIfNotExist(group_id, group_title):
    try:
        group_data = api.group.get(groupname=group_id)
    except ValueError:
        group_data = None

    if not group_data:
        api.group.create(groupname=group_id,
                         title=group_title)


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    for group_tuple in [(RV_MANAGERS_GID, 'RV Managers'),
                        (HOME_OWNERS_GID, 'Homeowners'),
                        (RENTERS_GID, 'Renters'),
                        (HOMEOWNER_AND_RENTER_GID, 'Homeowners and Renters')]:
        createGroupIfNotExist(group_tuple[0], group_tuple[1])



def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
