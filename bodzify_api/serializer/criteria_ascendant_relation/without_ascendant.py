#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
from bodzify_api.serializer.criteria_ascendant_relation.detailed \
    import CriteriaAscendantRelationDetailedSerializer, Fields as DETAILED_FIELDS


class Fields:
    DESCENDANT = DETAILED_FIELDS.DESCENDANT
    DEGREE = DETAILED_FIELDS.DEGREE


class CriteriaAscendantRelationWithoutAscendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRelation
        fields = [Fields.DESCENDANT, Fields.DEGREE]
