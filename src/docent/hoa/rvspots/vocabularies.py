# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import GroupNotFoundError
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer

from docent.hoa.rvspots.app_config import BOARD_MEMBERS_GID, PROPERTY_MANAGERS_GID, HOME_OWNERS_GID, HOMEOWNER_AND_RENTER_GID

from plone.memoize import ram
from time import time

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

    if member_fullname_by_id_dict:
        terms.append(SimpleVocabulary.createTerm('', '', 'Choose One'))
        for id_key, name_value in sorted(member_fullname_by_id_dict.iteritems(), key=lambda (k,v): (v,k)):
            terms.append(SimpleVocabulary.createTerm(id_key, str(id_key), name_value))
    else:
        terms.append(SimpleVocabulary.createTerm('', '', 'No Members'))

    return SimpleVocabulary(terms)


@ram.cache(lambda *args: time() // (60 * 60))
def getHomeOwnersVocabulary(group_name):
    """Return a set of groupmembers, return an empty set if group not found
    """

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

    if member_fullname_by_id_dict:
        terms.append(SimpleVocabulary.createTerm('', '', 'Choose One'))
        for id_key, name_value in sorted(member_fullname_by_id_dict.iteritems(), key=lambda (k,v): (v,k)):
            terms.append(SimpleVocabulary.createTerm(id_key, str(id_key), name_value))
    else:
        terms.append(SimpleVocabulary.createTerm('', '', 'No Members'))

    return SimpleVocabulary(terms)


@ram.cache(lambda *args: time() // (60 * 60))
def getHomeOwnersAndRentersVocabulary(group_name):
    """Return a set of groupmembers, return an empty set if group not found
    """

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

    if member_fullname_by_id_dict:
        terms.append(SimpleVocabulary.createTerm('', '', 'Choose One'))
        for id_key, name_value in sorted(member_fullname_by_id_dict.iteritems(), key=lambda (k,v): (v,k)):
            terms.append(SimpleVocabulary.createTerm(id_key, str(id_key), name_value))
    else:
        terms.append(SimpleVocabulary.createTerm('', '', 'No Members'))

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

