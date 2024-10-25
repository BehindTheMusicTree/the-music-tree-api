#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.criteria.output.fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.criteria_ascendant_relation.without_ascendant import \
    CriteriaAscendantRelationWithoutAscendantSerializer


class Fields:
    CREATED_ON = AvailableFields.CREATED_ON
    UPDATED_ON = AvailableFields.UPDATED_ON
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    PARENT = AvailableFields.PARENT
    DESCENDANTS = AvailableFields.DESCENDANTS


class CriteriaSimpleSerializer(serializers.ModelSerializer):
    parent = CriteriaMinimumSerializer()
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AvailableFields.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.PARENT,
                  Fields.DESCENDANTS,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
