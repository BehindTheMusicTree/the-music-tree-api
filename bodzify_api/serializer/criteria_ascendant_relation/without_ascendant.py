#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
from bodzify_api.serializer.criteria_ascendant_relation.detailed \
    import CriteriaAscendantRelationDetailedSerializer, FIELDS as DETAILED_FIELDS


class FIELDS:
    DESCENDANT = DETAILED_FIELDS.DESCENDANT
    DEGREE = DETAILED_FIELDS.DEGREE


class CriteriaAscendantRelationWithoutAscendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRelation
        fields = [FIELDS.DESCENDANT, FIELDS.DEGREE]
