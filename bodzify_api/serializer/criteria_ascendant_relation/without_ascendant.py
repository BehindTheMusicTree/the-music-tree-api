#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaAscendantRelation import CriteriaAscendantRelation
from bodzify_api.serializer.criteria_ascendant_relation.detailed \
    import CriteriaAscendantRelationDetailedSerializer, Fields as DetailedFields


class Fields:
    DESCENDANT = DetailedFields.DESCENDANT
    DEGREE = DetailedFields.DEGREE


class CriteriaAscendantRelationWithoutAscendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRelation
        fields = [Fields.DESCENDANT, Fields.DEGREE]
