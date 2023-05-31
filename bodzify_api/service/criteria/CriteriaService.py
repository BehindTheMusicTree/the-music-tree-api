#!/usr/bin/env python

from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.criteria.CriteriaPostSerializer import CriteriaPostSerializer


class CriteriaService:

    def create(self, criteriaType: int, playlistType: int, user: User, postData: QueryDict) -> Criteria:

        requestSerializer = CriteriaPostSerializer(data=postData)
        requestSerializer.is_valid(raise_exception=True)

        key = CRITERIA_ATTRIBUTES_LABEL.PARENT
        if key in requestSerializer.validated_data:
            parent = requestSerializer.validated_data[key]
        else:
            parent = None

        if parent in [None, ""]:
            parent = Criteria.objects.get(
                user=user, type=criteriaType, parent=None)

        criteria = requestSerializer.save(user=user,
                                          type=criteriaType,
                                          parent=parent)

        self.createLinkedPlaylist(user=user, criteria=criteria)
        Playlist(user=user, criteria=criteria, type=playlistType).save()

        return criteria

def GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
        user: User, criteriaName: str) -> Criteria:

    if Criteria.objects.filter(user=user, name=criteriaName).exists():
        criteria = Criteria.objects.get(user=user, name=criteriaName)
    else:
        criteria = Criteria.objects.create(user=user,
                                            type=CriteriaType.objects.get(
                                                id=CriteriaTypesId.GENRE),
                                            name=criteriaName)
        CriteriaPlaylist.objects.create(user=user, criteria=criteria)
    return criteria
