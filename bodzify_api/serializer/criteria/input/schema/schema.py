#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import AttributesLabels, Criteria


class Fields:
    NAME = AttributesLabels.NAME
    PARENT = AttributesLabels.PARENT


class CriteriaSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
