#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer
from bodzify_api.serializer.criteria.input.schema.CriteriaSaveSchemaSerializer \
    import CriteriaSaveSchemaSerializer, FIELDS as SAVE_SCHEMA_FIELDS


class FIELDS:
    NAME = SAVE_SCHEMA_FIELDS.NAME
    PARENT = SAVE_SCHEMA_FIELDS.PARENT


class CriteriaPostSerializer(CriteriaSaveSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = Criteria
        fields = [FIELDS.NAME, FIELDS.PARENT]
