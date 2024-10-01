#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria_ascendant_relation.without_ascendant \
    import CriteriaAscendantRelationWithoutAscendantSerializer


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    PARENT = AttributesLabel.PARENT
    DESCENDANTS = AttributesLabel.DESCENDANTS


class CriteriaWithDescendantsAndParentSerializer(serializers.ModelSerializer):
    parent = CriteriaSimpleSerializer()
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AttributesLabel.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.PARENT,
                  Fields.DESCENDANTS]
