#!/usr/bin/env python

from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
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
                parent = Criteria.objects.get(uuid=parent)
        else:
            parent = None

        saveData = data.copy()
        saveData[CRITERIA_ATTRIBUTES_LABEL.USER] = user.pk
        saveData[CRITERIA_ATTRIBUTES_LABEL.TYPE] = self.getCriteriaTypeId()
        saveData[CRITERIA_ATTRIBUTES_LABEL.PARENT] = parent.pk if parent is not None else ""
        saveData[CRITERIA_ATTRIBUTES_LABEL.ROOT] = parent.root if parent is not None else ""
        saveSerializer = CriteriaSaveModelSerializer(data=saveData)
        saveSerializer.is_valid(raise_exception=True)
        criteria = saveSerializer.save()

        CriteriaPlaylist(user=user, type_id=CriteriaTypesId.GENRE, criteria=criteria).save()

        return criteria
    
    def getCriteriaPlaylistClass(self):
        raise NotImplementedError("You should implement this method in a subclass")


    def getCriteriaFromNameAfterHavingEventuallyCreatedIt(
        self, user: User, criteriaName: str) -> Criteria:

        if Criteria.objects.filter(user=user, type_id=self.getCriteriaTypeId(), name=criteriaName).exists():
            criteria = Criteria.objects.get(user=user, type_id=self.getCriteriaTypeId(), name=criteriaName)
        else:
            criteria = Criteria.objects.create(
                user=user, type_id=self.getCriteriaTypeId(), name=criteriaName)
            CriteriaPlaylist(user=user, type_id=CriteriaTypesId.GENRE, criteria=criteria).save()    
        return criteria

    def getCriteriaTypeId(self):
        raise NotImplementedError("You should implement this method in a subclass")