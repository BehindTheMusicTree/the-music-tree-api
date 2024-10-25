#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.criteria.input.schema.schema import CriteriaSchemaSerializer, Fields as SchemaFields
from bodzify_api.serializer.schema.endpoint import InputEndpointSerializer


class Fields:
    NAME = SchemaFields.NAME
    PARENT = SchemaFields.PARENT


class CriteriaPostSerializer(CriteriaSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
