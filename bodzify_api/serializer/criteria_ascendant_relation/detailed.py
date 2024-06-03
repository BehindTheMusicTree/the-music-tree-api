#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaAscendantRelation import ATTRIBUTES_LABEL, CriteriaAscendantRelation
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer


class FIELDS:
    DESCENDANT = ATTRIBUTES_LABEL.DESCENDANT
    ASCENDANT = ATTRIBUTES_LABEL.ASCENDANT
    DEGREE = ATTRIBUTES_LABEL.DEGREE


class CriteriaAscendantRelationDetailedSerializer(serializers.ModelSerializer):
    descendant = CriteriaSimpleSerializer()
    ascendant = CriteriaSimpleSerializer()

    class Meta:
        model = CriteriaAscendantRelation
        fields = [FIELDS.DESCENDANT, FIELDS.ASCENDANT, FIELDS.DEGREE]
