#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.criteria.input.schema.schema import CriteriaSchemaSerializer, Fields as SaveSchemaFields


class Fields:
    NAME = SaveSchemaFields.NAME
    PARENT = SaveSchemaFields.PARENT


class CriteriaPostSerializer(CriteriaSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
