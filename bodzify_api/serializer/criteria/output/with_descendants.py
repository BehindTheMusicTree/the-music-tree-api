#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel
from bodzify_api.serializer.criteria_ascendant_relation.without_ascendant \
    import CriteriaAscendantRelationWithoutAscendantSerializer


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    DESCENDANTS = AttributesLabel.DESCENDANTS


class CriteriaWithDescendantsSerializer(serializers.ModelSerializer):
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AttributesLabel.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.DESCENDANTS]
