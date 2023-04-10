#!/usr/bin/env python
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, CriteriaSpecialNames, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaType
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType
from bodzify_api.model.playlist.PlaylistType import PlaylistTypesId
from bodzify_api.serializer.criteria.CriteriaPostSerializer import CriteriaPostSerializer


def Create(criteriaTypeId: int, playlistTypeId: int, user: User, postData: QueryDict) -> Criteria:

    requestSerializer = CriteriaPostSerializer(data=postData)
    requestSerializer.is_valid(raise_exception=True)

    key = CRITERIA_ATTRIBUTES_LABEL.PARENT
    if key in requestSerializer.validated_data:
        parent = requestSerializer.validated_data[key]
    else:
        parent = None

    if parent in [None, ""]:
        parent = Criteria.objects.get(
            user=user, type=criteriaTypeId, parent=None)

    criteria = requestSerializer.save(
        user=user,
        type=criteriaTypeId,
        parent=parent)

    Playlist(user=user, criteria=criteria, type=playlistTypeId).save()
    
    return criteria


def GetCriteriaFromNameAfterHavingEventuallyCreatedIt(
        user: User, criteriaName: str) -> Criteria:
    if Criteria.objects.filter(user=user, name=criteriaName).exists():
        criteria = Criteria.objects.get(user=user, name=criteriaName)
    else:
        criteria = Criteria.objects.create(
            user=user,
            type=CriteriaType.objects.get(id=CriteriaTypesId.GENRE),
            name=criteriaName,
            parent=Criteria.objects.get(
                user=user, name=CriteriaSpecialNames.GENRE_ALL)
        )
        Playlist.objects.create(
            user=user,
            criteria=criteria,
            type=PlaylistType.objects.get(pk=PlaylistTypesId.GENRE)
        )
    return criteria
