#!/usr/bin/env python

import logging
from django.contrib.auth.models import User
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.input.CriteriaModelSerializer import CriteriaSaveModelSerializer
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import CriteriaPutSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer import CriteriaSaveSchemaSerializer

from bodzify_api.service.Service import Service


class CriteriaService(Service):

    def __init__(self, criteria_type_id) -> None:
        self.criteria_type_id = criteria_type_id
        super().__init__()

    def _get_post_serializer(self, post_data: dict):
        return CriteriaSaveSchemaSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return CriteriaPutSerializer(instance=old_instance, data=put_data)

    def _get_save_schema_serializer(self, old_instance, save_schema_data: dict, request):
        return CriteriaSaveSchemaSerializer(data=save_schema_data, context={'request': request})

    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool):
        return CriteriaSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True)

    def _get_save_schema_data_from_post_data(self, post_data: dict) -> dict:
        save_schema_data = post_data.copy()

        parent_key = CRITERIA_ATTRIBUTES_LABEL.PARENT
        if parent_key in post_data:
            parent_uuid = post_data[parent_key]
            if parent_uuid in ["", None]:
                parent_uuid = ""
        else:
            parent_uuid = ""
        save_schema_data[CRITERIA_ATTRIBUTES_LABEL.PARENT] = parent_uuid
        return save_schema_data

    def _get_save_schema_data_from_put_data(self, put_data: dict, old_instance) -> dict:
        return put_data

    def _get_save_model_data_from_save_schema_data_not_including_user_field(
            self, user: User, save_schema_data: dict, old_instance) -> dict:
        save_model_data = dict()

        self._update_data1_with_key_if_set_in_data2(key=CRITERIA_ATTRIBUTES_LABEL.NAME,
                                                    data1=save_model_data,
                                                    data2=save_schema_data)

        self._update_data1_with_key_if_set_in_data2(key=CRITERIA_ATTRIBUTES_LABEL.PARENT,
                                                    data1=save_model_data,
                                                    data2=save_schema_data)

        save_model_data[CRITERIA_ATTRIBUTES_LABEL.TYPE] = self.criteria_type_id

        return save_model_data
