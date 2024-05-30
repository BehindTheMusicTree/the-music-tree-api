#!/usr/bin/env python

import logging
from django.contrib.auth.models import User
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.input.model import CriteriaModelSerializer
from bodzify_api.serializer.criteria.input.schema.endpoint.put import CriteriaPutSerializer
from bodzify_api.serializer.criteria.input.schema.schema import CriteriaSchemaSerializer

from bodzify_api.service.Service import Service


class CriteriaService(Service):

    def __init__(self, criteria_type_id) -> None:
        self.criteria_type_id = criteria_type_id
        super().__init__()

    def _get_post_serializer(self, post_data: dict):
        return CriteriaSchemaSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return CriteriaPutSerializer(instance=old_instance, data=put_data)

    def _get_schema_serializer(self, old_instance, schema_data: dict, request):
        return CriteriaSchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, old_instance, model_data: dict, partial: bool):
        return CriteriaModelSerializer(instance=old_instance, data=model_data, partial=True)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        schema_data = post_data.copy()

        parent_key = ATTRIBUTES_LABEL.PARENT
        if parent_key in post_data:
            parent_uuid = post_data[parent_key]
            if parent_uuid in ["", None]:
                parent_uuid = ""
        else:
            parent_uuid = ""
        schema_data[ATTRIBUTES_LABEL.PARENT] = parent_uuid
        return schema_data

    def _get_schema_data_from_put_data(self, put_data: dict, old_instance) -> dict:
        return put_data

    def _get_model_data_from_schema_data_not_including_user_field(
            self, user: User, schema_data: dict, old_instance) -> dict:
        model_data = dict()

        self._update_data1_with_key_if_set_in_data2(key=ATTRIBUTES_LABEL.NAME,
                                                    data1=model_data,
                                                    data2=schema_data)

        self._update_data1_with_key_if_set_in_data2(key=ATTRIBUTES_LABEL.PARENT,
                                                    data1=model_data,
                                                    data2=schema_data)

        model_data[ATTRIBUTES_LABEL.TYPE] = self.criteria_type_id

        return model_data
