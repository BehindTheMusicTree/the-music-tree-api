#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.CriteriaType import CriteriaType, AttributesLabel


class FIELDS:
    LABEL = AttributesLabel.LABEL


class CriteriaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CriteriaType
        fields = [FIELDS.LABEL]
