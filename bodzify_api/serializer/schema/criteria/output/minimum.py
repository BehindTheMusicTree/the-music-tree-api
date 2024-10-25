#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.criteria.output.fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class CriteriaMinimumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,]
