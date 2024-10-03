#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabels
from rest_framework import serializers


class Fields:
    NAME = AttributesLabels.NAME
    PARENT = AttributesLabels.PARENT


class CriteriaSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
