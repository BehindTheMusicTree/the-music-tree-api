#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
from bodzify_api.serializer.criteria_ascendant_relation.detailed \
    import CriteriaAscendantRelationDetailedSerializer, Fields as DETAILED_FIELDS


class Fields:
    ASCENDANT = DETAILED_FIELDS.ASCENDANT
    DEGREE = DETAILED_FIELDS.DEGREE


class CriteriaAscendantRelationWithoutDescendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRelation
        fields = [Fields.ASCENDANT, Fields.DEGREE]
