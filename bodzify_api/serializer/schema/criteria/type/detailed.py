#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaType import CriteriaType, Fields as ModelFields


class Fields:
    LABEL = ModelFields.LABEL


class CriteriaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CriteriaType
        fields = [Fields.LABEL]
