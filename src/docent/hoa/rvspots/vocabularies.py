# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import GroupNotFoundError
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer
from datetime import datetime

import json

from docent.hoa.rvspots.app_config import BOARD_MEMBERS_GID, PROPERTY_MANAGERS_GID, HOME_OWNERS_GID, HOMEOWNER_AND_RENTER_GID, DATE_STRING
from docent.hoa.rvspots.interfaces import IStoreVocabularyData
from plone.memoize import ram
from time import time


def rebuildVocabulary(date_string):
    last_rebuild = datetime.strptime(date_string, DATE_STRING)
    delta_out = datetime.today() - last_rebuild
    if delta_out.days >= 5:
        return True
    return False

def getGroupMemberVocabulary(group_name, multi_group=False):
    """Return a set of groupmembers, return an empty set if group not found
    """
    if multi_group:
        group_members = []
        try:
            sub_groups = api.user.get_users(groupname=group_name)
        except GroupNotFoundError:
            sub_groups = []
        for sub_group in sub_groups:
            try:
                sub_group_members = api.user.get_users(group=sub_group)
            except GroupNotFoundError:
                sub_group_members = []
            group_members += sub_group_members
    else:
        try:
            group_members = api.user.get_users(groupname=group_name)
        except GroupNotFoundError:
            group_members = []

    member_fullname_by_id_dict = {}
    for member_data in set(group_members):
        member_id = member_data.getId()
        member_fullname = member_data.getProperty('fullname')
        member_fullname_by_id_dict.update({member_id:member_fullname})

    terms = []
    stored_terms = []
    if member_fullname_by_id_dict:
        terms.append(SimpleVocabulary.createTerm('', '', 'Choose One'))
        for id_key, name_value in sorted(member_fullname_by_id_dict.iteritems(), key=lambda (k,v): (v,k)):
            stored_terms.append((id_key, str(id_key), name_value))
            terms.append(SimpleVocabulary.createTerm(id_key, str(id_key), name_value))
    else:
        stored_terms.append(('', '', 'No Members'))
        terms.append(SimpleVocabulary.createTerm('', '', 'No Members'))

    return SimpleVocabulary(terms)


# @ram.cache(lambda *args: time() // (60 * 60))
def getHomeOwnersVocabulary(group_name):
    """Return a set of groupmembers, return an empty set if group not found
    """

    home_owners_last_build_date = api.portal.get_registry_record(name='home_owners_last_build_date',
                                                                 interface=IStoreVocabularyData,
                                                                 default='')
    rebuild = False
    if not home_owners_last_build_date:
        rebuild = True
    else:
        rebuild = rebuildVocabulary(home_owners_last_build_date)

    if rebuild:
        group_members = []
        try:
            sub_groups = api.user.get_users(groupname=group_name)
        except GroupNotFoundError:
            sub_groups = []
        for sub_group in sub_groups:
            try:
                sub_group_members = api.user.get_users(group=sub_group)
            except GroupNotFoundError:
                sub_group_members = []
            group_members += sub_group_members

        member_fullname_by_id_dict = {}
        for member_data in set(group_members):
            member_id = member_data.getId()
            member_fullname = member_data.getProperty('fullname')
            member_fullname_by_id_dict.update({member_id:member_fullname})

        terms = []
        stored_terms = []
        if member_fullname_by_id_dict:
            terms.append(SimpleVocabulary.createTerm('', '', 'Choose One'))
            for id_key, name_value in sorted(member_fullname_by_id_dict.iteritems(), key=lambda (k,v): (v,k)):
                stored_terms.append((id_key, str(id_key), name_value))
                terms.append(SimpleVocabulary.createTerm(id_key, str(id_key), name_value))
        else:
            stored_terms.append(('', '', 'No Members'))
            terms.append(SimpleVocabulary.createTerm('', '', 'No Members'))
        
        api.portal.set_registry_record(name='home_owners_tuples_json',
                                       value=u'%s' % json.dumps(stored_terms),
                                       interface=IStoreVocabularyData)

        api.portal.set_registry_record(name='home_owners_last_build_date',
                                       value=datetime.today().strftime(DATE_STRING),
                                       interface=IStoreVocabularyData)

    else:
        home_owners_tuples_json = api.portal.get_registry_record(name='home_owners_tuples_json',
                                                                 interface=IStoreVocabularyData,
                                                                 default = u'[]')
        home_owners_tuples = json.loads(home_owners_tuples_json)
        terms = []
        for ho_tuple in home_owners_tuples:
            id_key, id_str, name_value = ho_tuple
            terms.append(SimpleVocabulary.createTerm(id_key, id_str, name_value))

    return SimpleVocabulary(terms)


# @ram.cache(lambda *args: time() // (60 * 60))
def getHomeOwnersAndRentersVocabulary(group_name):
    """Return a set of groupmembers, return an empty set if group not found
    """
    renter_last_build_date = api.portal.get_registry_record(name='renter_last_build_date',
                                                                 interface=IStoreVocabularyData,
                                                                 default='')
    rebuild = False
    if not renter_last_build_date:
        rebuild = True
    else:
        rebuild = rebuildVocabulary(renter_last_build_date)

    if rebuild:
        group_members = []
        try:
            sub_groups = api.user.get_users(groupname=group_name)
        except GroupNotFoundError:
            sub_groups = []
        for sub_group in sub_groups:
            try:
                sub_group_members = api.user.get_users(group=sub_group)
            except GroupNotFoundError:
                sub_group_members = []
            group_members += sub_group_members

        member_fullname_by_id_dict = {}
        for member_data in set(group_members):
            member_id = member_data.getId()
            member_fullname = member_data.getProperty('fullname')
            member_fullname_by_id_dict.update({member_id:member_fullname})

        terms = []
        stored_terms = []
        if member_fullname_by_id_dict:
            terms.append(SimpleVocabulary.createTerm('', '', 'Choose One'))
            for id_key, name_value in sorted(member_fullname_by_id_dict.iteritems(), key=lambda (k,v): (v,k)):
                stored_terms.append((id_key, str(id_key), name_value))
                terms.append(SimpleVocabulary.createTerm(id_key, str(id_key), name_value))
        else:
            stored_terms.append(('', '', 'No Members'))
            terms.append(SimpleVocabulary.createTerm('', '', 'No Members'))

        api.portal.set_registry_record(name='renters_tuples_json',
                                       value=u'%s' % json.dumps(stored_terms),
                                       interface=IStoreVocabularyData)

        api.portal.set_registry_record(name='renter_last_build_date',
                                       value=datetime.today().strftime(DATE_STRING),
                                       interface=IStoreVocabularyData)

    else:
        renters_tuples_json = api.portal.get_registry_record(name='renters_tuples_json',
                                                                 interface=IStoreVocabularyData,
                                                                 default=u'[]')
        renters_tuples = json.loads(renters_tuples_json)
        terms = []
        for ro_tuple in renters_tuples:
            id_key, id_str, name_value = ro_tuple
            terms.append(SimpleVocabulary.createTerm(id_key, id_str, name_value))

    return SimpleVocabulary(terms)

@implementer(IVocabularyFactory)
class IHomeOwnersVocabulary(object):
    def __call__(self, context):
        return getHomeOwnersVocabulary(HOME_OWNERS_GID)
IHomeOwnersVocabularyFactory = IHomeOwnersVocabulary()

@implementer(IVocabularyFactory)
class IHomnerRenterVocabulary(object):
    def __call__(self, context):
        return getHomeOwnersAndRentersVocabulary(HOMEOWNER_AND_RENTER_GID)
IHomnerRenterVocabularyFactory = IHomnerRenterVocabulary()

