#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaAscendantRel import AttributesLabels, CriteriaAscendantRel
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer


class Fields:
    DESCENDANT = AttributesLabels.DESCENDANT
    ASCENDANT = AttributesLabels.ASCENDANT
    DEGREE = AttributesLabels.DEGREE


class CriteriaAscendantRelationDetailedSerializer(serializers.ModelSerializer):
    descendant = CriteriaSimpleSerializer()
    ascendant = CriteriaSimpleSerializer()

    class Meta:
        model = CriteriaAscendantRel
        fields = [Fields.DESCENDANT, Fields.ASCENDANT, Fields.DEGREE]
