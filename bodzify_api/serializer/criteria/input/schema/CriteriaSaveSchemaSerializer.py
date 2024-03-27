#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT


class CriteriaSaveSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [FIELDS.NAME, FIELDS.PARENT]
