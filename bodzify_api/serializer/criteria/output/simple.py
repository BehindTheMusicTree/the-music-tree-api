#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel


class FIELDS:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    CREATED_ON = AttributesLabel.CREATED_ON


class CriteriaSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON]
