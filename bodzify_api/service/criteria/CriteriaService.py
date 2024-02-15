#!/usr/bin/env python

import logging
from django.contrib.auth.models import User
from django.http import QueryDict
from bodzify_api.model.criteria.Criteria import Criteria, \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.input.schema.CriteriaPostSchemaSerializer import CriteriaPostSchemaSerializer
from bodzify_api.serializer.criteria.input.CriteriaSaveModelSerializer import CriteriaSaveModelSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaUpdateSchemaSerializer import CriteriaPutSchemaSerializer

from bodzify_api.service.Service import Service
from rest_framework.serializers import Serializer

logger = logging.getLogger('bodzify_api')

class CriteriaService(Service):

    def get_criteria_from_name_after_having_eventually_created_it(
        self, user: User, criteria_name: str) -> Criteria:

        if Criteria.objects.filter(user=user, type_id=self.get_criteria_type_id(), name=criteria_name).exists():
            criteria = Criteria.objects.get(user=user, type_id=self.get_criteria_type_id(), name=criteria_name)
        else:
            criteria = Criteria.objects.create(user=user, type_id=self.get_criteria_type_id(), name=criteria_name)
        return criteria

    def _get_post_schema_serializer(self, post_schema_data: QueryDict):
        return CriteriaPostSchemaSerializer(data=post_schema_data) # type: ignore

    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
        return CriteriaPutSchemaSerializer(instance=old_instance, data=put_schema_data) # type: ignore

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        return CriteriaSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True) # type: ignore

    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        save_schema_data = post_schema_data.copy()

        parent_key = CRITERIA_ATTRIBUTES_LABEL.PARENT
        if parent_key in post_schema_data:
            parent_uuid = post_schema_data[parent_key]
            if parent_uuid in ["", None]:
                parent_uuid = ""
        else:
            parent_uuid = ""
        save_schema_data[CRITERIA_ATTRIBUTES_LABEL.PARENT] = parent_uuid
        return save_schema_data
    
    def _get_save_model_data_from_save_schema_data(self, user: User, save_schema_data: QueryDict) -> QueryDict:
        save_model_data = QueryDict(mutable=True)
        save_model_data[CRITERIA_ATTRIBUTES_LABEL.USER] = user.pk

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=CRITERIA_ATTRIBUTES_LABEL.NAME,
            querydict1=save_model_data,
            querydict2=save_schema_data)

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=CRITERIA_ATTRIBUTES_LABEL.PARENT,
            querydict1=save_model_data,
            querydict2=save_schema_data)
        
        save_model_data[CRITERIA_ATTRIBUTES_LABEL.TYPE] = self.get_criteria_type_id()

        return save_model_data

    def get_criteria_playlist_class(self):
        raise NotImplementedError("You should implement this method in a subclass")

    def get_criteria_type_id(self):
        raise NotImplementedError("You should implement this method in a subclass")