#!/usr/bin/env python

from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.criteria.input.CriteriaPostSchemaSerializer import CriteriaPostSchemaSerializer
from bodzify_api.serializer.criteria.input.CriteriaSaveModelSerializer import CriteriaSaveModelSerializer


class CriteriaService:

    def create(self, user: User, data: QueryDict) -> Criteria:

        schemaSerializer = CriteriaPostSchemaSerializer(data=data)
        schemaSerializer.is_valid(raise_exception=True)

        parentKey = CRITERIA_ATTRIBUTES_LABEL.PARENT
        if parentKey in schemaSerializer.validated_data:
            parent = schemaSerializer.validated_data[parentKey]
            if parent == "":
                parent = None
        else:
            parent = None
            
        saveData = data.copy()
        saveData[CRITERIA_ATTRIBUTES_LABEL.USER] = user.id
        saveData[CRITERIA_ATTRIBUTES_LABEL.TYPE] = self.getTypeId()
        saveData[CRITERIA_ATTRIBUTES_LABEL.PARENT] = parent
        saveSerializer = CriteriaSaveModelSerializer(data=saveData)
        saveSerializer.is_valid(raise_exception=True)
        criteria = saveSerializer.save()

        self.createLinkedPlaylist(user=user, criteria=criteria)
        criteriaPlaylistClass = self.getCriteriaPlaylistClass()
        criteriaPlaylistClass(user=user, criteria=criteria).save()

        return criteria
    
    def getCriteriaPlaylistClass(self):
        raise NotImplementedError("You should implement this method in a subclass")


    def getCriteriaFromNameAfterHavingEventuallyCreatedIt(
        self, user: User, criteriaName: str) -> Criteria:

        if Criteria.objects.filter(user=user, type_id=self.getTypeId(), name=criteriaName).exists():
            criteria = Criteria.objects.get(user=user, type_id=self.getTypeId(), name=criteriaName)
        else:
            criteria = Criteria.objects.create(
                user=user, type_id=self.getTypeId(), name=criteriaName)
            self.createLinkedPlaylist(user=user, criteria=criteria)
        return criteria

    def getTypeId(self):
        raise NotImplementedError("You should implement this method in a subclass")

    def createLinkedPlaylist(self, user: User, criteria: Criteria):
        raise NotImplementedError("You should implement this method in a subclass")