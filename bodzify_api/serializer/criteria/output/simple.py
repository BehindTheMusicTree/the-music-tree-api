#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import AttributesLabels, Criteria


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME


class CriteriaSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,]
