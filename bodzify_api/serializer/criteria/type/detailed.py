#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.CriteriaType import CriteriaType, AttributesLabels


class Fields:
    LABEL = AttributesLabels.LABEL


class CriteriaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CriteriaType
        fields = [Fields.LABEL]
