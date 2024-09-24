#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaAscendantRelation import AttributesLabel, CriteriaAscendantRelation
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer


class FIELDS:
    DESCENDANT = AttributesLabel.DESCENDANT
    ASCENDANT = AttributesLabel.ASCENDANT
    DEGREE = AttributesLabel.DEGREE


class CriteriaAscendantRelationDetailedSerializer(serializers.ModelSerializer):
    descendant = CriteriaSimpleSerializer()
    ascendant = CriteriaSimpleSerializer()

    class Meta:
        model = CriteriaAscendantRelation
        fields = [FIELDS.DESCENDANT, FIELDS.ASCENDANT, FIELDS.DEGREE]
