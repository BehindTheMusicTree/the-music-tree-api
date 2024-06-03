#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaAscendantRelation import ATTRIBUTES_LABEL, CriteriaAscendantRelation
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer


class FIELDS:
    CHILD = ATTRIBUTES_LABEL.CHILD
    ASCENDANT = ATTRIBUTES_LABEL.ASCENDANT
    DEGREE = ATTRIBUTES_LABEL.DEGREE


class CriteriaAscendantRelationDetailedSerializer(serializers.ModelSerializer):
    child = CriteriaSimpleSerializer()
    ascendant = CriteriaSimpleSerializer()

    class Meta:
        model = CriteriaAscendantRelation
        fields = [FIELDS.CHILD, FIELDS.ASCENDANT, FIELDS.DEGREE]
