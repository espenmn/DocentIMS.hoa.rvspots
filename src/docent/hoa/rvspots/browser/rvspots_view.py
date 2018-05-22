# -*- coding: utf-8 -*-
from plone import api
#from Products.Five.browser import BrowserView
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.protect.utils import addTokenToUrl

import logging
logger = logging.getLogger("Plone")

class RVSpotsView(BrowserView):

    index = ViewPageTemplateFile('templates/rvspots_view.pt')

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        content_items = self.context.contentItems()
        current_member_data = api.user.get_current()
        current_member_id = current_member_data.getId()

        spots = [i[1] for i in content_items]

        modified_DateTimes = [s.modified() for s in spots]
        if modified_DateTimes:
            sorted_DateTimes = sorted(modified_DateTimes)
            last_modified_DT = sorted_DateTimes[-1]
            self.last_updated = last_modified_DT.strftime('%b %d %Y - %H:%M:%S')
        else:
            self.last_updated = ''

        self.spots = spots
        self.current_member_data = current_member_data
        self.current_member_id = current_member_id

    def getSpots(self):
        return self.spots

    def hasEditPermissions(self):
        #who can edit? Managers, Site Administrators, RV Managers
        return api.user.has_permission('Modify portal content', user=self.current_member_data, obj=self.context)

    def hasView(self):
        if self.hasEditPermissions():
            return False
        return True

    def getOwnerEmail(self, spot_obj):
        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        if owner_id:
            owner_data = api.user.get(userid=owner_id)
            return owner_data.getProperty('email')
        else:
            return ''

    def getOwnerFullname(self, spot_obj):
        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        if owner_id:
            owner_data = api.user.get(userid=owner_id)
            return owner_data.getProperty('fullname')
        else:
            return ''

    def getRenterEmail(self, spot_obj):
        renter_id = getattr(spot_obj, 'renter', '') or ''
        if renter_id:
            renter_data = api.user.get(userid=renter_id)
            return renter_data.getProperty('email')
        else:
            return ''

    def getRenterFullname(self, spot_obj):
        renter_id = getattr(spot_obj, 'renter', '') or ''
        if renter_id:
            renter_data = api.user.get(userid=renter_id)
            return renter_data.getProperty('fullname')
        else:
            return ''

    def getUnmanagedOwner(self, spot_obj):
        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        if not owner_id:
            return 'Unassigned'
        else:
            if self.current_member_id == owner_id:
                return self.current_member_data.getProperty('fullname')
            else:
                return "Assigned"

    def getUnmanagedRenter(self, spot_obj):
        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        renter_id = getattr(spot_obj, 'renter', '') or ''

        if not renter_id:
            return 'Unassigned'
        else:
            if self.current_member_id in [owner_id, renter_id]:
                renter_data = api.user.get(userid=renter_id)
                return renter_data.getProperty('fullname')
            else:
                return "Assigned"

    def isContractOwner(self, spot_obj):
        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        if self.current_member_id == owner_id:
            return True
        return False

    def isContractRenter(self, spot_obj):
        renter_id = getattr(spot_obj, 'renter', '') or ''
        if self.current_member_id == renter_id:
            return True
        return False

    def getOwnerContractURL(self, spot_obj):
        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        if self.current_member_id == owner_id:
            hc_obj = getattr(spot_obj, 'homeowner_contract', None) or None
            if not hc_obj:
                return ''
            filename = hc_obj.filename
            return '%s/@@download/homeowner_contract/%s' % (self.context.absolute_url(), filename)

    def getRenterContractURL(self, spot_obj):
        renter_id = getattr(spot_obj, 'renter', '') or ''
        if self.current_member_id == renter_id:
            rc_obj = getattr(spot_obj, 'renter_contract', None) or None
            if not rc_obj:
                return ''
            filename = rc_obj.filename
            return '%s/@@download/homeowner_contract/%s' % (self.context.absolute_url(), filename)

    def getUnmanagedInsurance(self, spot_obj):
        renter_id = getattr(spot_obj, 'renter', '') or ''
        if self.current_member_id == renter_id:
            if_obj = getattr(spot_obj, 'insurance_file', None) or None
            if not if_obj:
                return ''
            filename = if_obj.filename
            return '%s/@@download/insurance_file/%s' % (self.context.absolute_url(), filename)

    def getUnmanagedOccupancy(self, spot_obj):
        occupancy = getattr(spot_obj, 'occupancy', None) or None
        if not occupancy:
            return None

        owner_id = getattr(spot_obj, 'homeowner', '') or ''
        renter_id = getattr(spot_obj, 'renter', '') or ''

        if self.current_member_id in [owner_id, renter_id]:
            return occupancy.strftime("%B %-d, %Y")
        else:
            return "Assigned"

    def getClearURL(self, spot_obj):
        spot_url = '%s/clear_spot' % spot_obj.absolute_url()
        return addTokenToUrl(spot_url)
