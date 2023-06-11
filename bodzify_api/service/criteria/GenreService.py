#!/usr/bin/env python
from django.contrib.auth.models import User
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.service.criteria.CriteriaService import CriteriaService


class GenreService(CriteriaService):
    
    def createLinkedPlaylist(self, user: User, criteria: Criteria):
        GenrePlaylist(user=user, criteria=criteria).save()
        
    def getTypeId(self):
        return CriteriaTypesId.GENRE
    
    def getCriteriaPlaylistClass(self):
        return GenrePlaylist
