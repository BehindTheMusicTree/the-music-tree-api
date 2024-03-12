#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON


class CriteriaSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON]
