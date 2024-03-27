#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT


class CriteriaSaveSchemaSerializer(InputModelSerializer):

    class Meta:
        model = Criteria
        fields = [FIELDS.NAME, FIELDS.PARENT]
