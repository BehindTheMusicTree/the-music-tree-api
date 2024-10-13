#!/usr/bin/env python

from bodzify_api.serializer.criteria_ascendant_relation.detailed import Fields as DetailedFields
from bodzify_api.serializer.criteria_ascendant_relation.detailed import CriteriaAscendantRelationDetailedSerializer
from bodzify_api.model.criteria.CriteriaAscendantRel import CriteriaAscendantRel


class Fields:
    DESCENDANT = DetailedFields.DESCENDANT
    DEGREE = DetailedFields.DEGREE


class CriteriaAscendantRelationWithoutAscendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRel
        fields = [Fields.DESCENDANT, Fields.DEGREE]
