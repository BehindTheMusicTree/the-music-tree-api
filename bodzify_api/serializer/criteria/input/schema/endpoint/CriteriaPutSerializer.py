#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaSchemaSerializer \
    import CriteriaSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS


class FIELDS:
    NAME = SAVE_SCHEMA_FIELDS.NAME
    PARENT = SAVE_SCHEMA_FIELDS.PARENT


class CriteriaPutSerializer(CriteriaSaveSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = Criteria
        fields = [FIELDS.NAME, FIELDS.PARENT]

    def validate_parent(self, value):
        instance = self.instance

        if instance and value:
            if instance == value:
                raise serializers.ValidationError("Cannot set the new parent as the criteria itself.")
            elif value.is_descendant_of(instance):
                raise serializers.ValidationError("Cannot set the new parent as one of the criteria's descendants.")
        return value
