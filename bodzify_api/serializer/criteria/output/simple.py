#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    CREATED_ON = AttributesLabel.CREATED_ON


class CriteriaSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CREATED_ON]
