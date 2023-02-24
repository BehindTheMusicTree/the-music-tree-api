#!/usr/bin/env python
from django.contrib.auth.models import User
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesIds
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeIds


def GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
          user: User, criteriaName: str) -> Criteria:
    if Criteria.objects.filter(
            user=user, 
            type__id=CriteriaTypesIds.GENRE, 
            name=criteriaName
        ).exists():
            criteria = Criteria.objects.get(
                    user=user, type__id=CriteriaTypesIds.GENRE, name=criteriaName)
    else:
        criteria = Criteria.objects.create(
            user=user,
            type=CriteriaType.objects.get(id=CriteriaTypesIds.GENRE),
            name=criteriaName,
            parent=Criteria.objects.get(user=user, name=CriteriaSpecialNames.GENRE_ALL)
        )
        Playlist.objects.create(
            user=user,
            criteria=criteria,
            type=PlaylistType.objects.get(pk=PlaylistTypeIds.GENRE)
        )
    return criteria