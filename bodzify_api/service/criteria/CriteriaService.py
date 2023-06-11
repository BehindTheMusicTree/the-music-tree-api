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

    def create(self, user: User, data: QueryDict) -> Criteria:

        postSerializer = CriteriaPostSerializer(data=data)
        postSerializer.is_valid(raise_exception=True)

        parentKey = CRITERIA_ATTRIBUTES_LABEL.PARENT
        if parentKey in postSerializer.validated_data:
            parent = postSerializer.validated_data[parentKey]
            if parent == "":
                parent = None
        else:
            parent = None

        criteria = postSerializer.save(user=user, parent=parent, type_id=self.getTypeId())

        self.createLinkedPlaylist(user=user, criteria=criteria)
        criteriaPlaylistClass = self.getCriteriaPlaylistClass()
        criteriaPlaylistClass(user=user, criteria=criteria).save()

        return criteria
    
    def getCriteriaPlaylistClass(self):
        raise NotImplementedError("You should implement this method in a subclass")


    def getCriteriaFromNameAfterHavingEventuallyCreatedIt(
        self, user: User, criteriaName: str) -> Criteria:

        if Criteria.objects.filter(user=user, name=criteriaName).exists():
            criteria = Criteria.objects.get(user=user, name=criteriaName)
        else:
            criteria = Criteria.objects.create(
                user=user, type=self.getTypeId(), name=criteriaName)
            CriteriaPlaylist.objects.create(user=user, criteria=criteria)
        return criteria

    def getTypeId(self):
        raise NotImplementedError("You should implement this method in a subclass")

    def createLinkedPlaylist(self, user: User, criteria: Criteria):
        raise NotImplementedError("You should implement this method in a subclass")