#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.CriteriaType import CriteriaType, ATTRIBUTES_LABEL


class FIELDS:
    LABEL = ATTRIBUTES_LABEL.LABEL


class CriteriaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CriteriaType
        fields = [FIELDS.LABEL]
