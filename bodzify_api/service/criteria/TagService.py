#!/usr/bin/env python

from django.contrib.auth.models import User
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.criteria.TagPlaylist import TagPlaylist


class TagService:
    
    def createLinkedPlaylist(self, user: User, criteria: Criteria):
        TagPlaylist(user=user, criteria=criteria).save()
        
    def getType(self):
        return CriteriaTypesId.TAG
