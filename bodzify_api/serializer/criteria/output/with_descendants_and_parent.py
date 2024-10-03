#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabels
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria_ascendant_relation.without_ascendant \
    import CriteriaAscendantRelationWithoutAscendantSerializer


class Fields:
    UUID = AttributesLabels.UUID
    CREATED_ON = AttributesLabels.CREATED_ON
    UPDATED_ON = AttributesLabels.UPDATED_ON
    NAME = AttributesLabels.NAME
    PARENT = AttributesLabels.PARENT
    DESCENDANTS = AttributesLabels.DESCENDANTS


class CriteriaWithDescendantsAndParentSerializer(serializers.ModelSerializer):
    parent = CriteriaSimpleSerializer()
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AttributesLabels.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.NAME,
                  Fields.PARENT,
                  Fields.DESCENDANTS]
