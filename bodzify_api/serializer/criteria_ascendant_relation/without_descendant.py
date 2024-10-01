#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
from bodzify_api.serializer.criteria_ascendant_relation.detailed \
    import CriteriaAscendantRelationDetailedSerializer, Fields as DetailedFields


class Fields:
    ASCENDANT = DetailedFields.ASCENDANT
    DEGREE = DetailedFields.DEGREE


class CriteriaAscendantRelationWithoutDescendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRelation
        fields = [Fields.ASCENDANT, Fields.DEGREE]
