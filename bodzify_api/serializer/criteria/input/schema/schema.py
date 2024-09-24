#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel
from rest_framework import serializers


class Fields:
    NAME = AttributesLabel.NAME
    PARENT = AttributesLabel.PARENT


class CriteriaSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
