#!/usr/bin/env python

from bodzify_api.model.criteria.CriteriaAscendantRel import CriteriaAscendantRel
from bodzify_api.serializer.criteria_ascendant_relation.detailed import CriteriaAscendantRelationDetailedSerializer
from bodzify_api.serializer.criteria_ascendant_relation.detailed import Fields as DetailedFields


class Fields:
    ASCENDANT = DetailedFields.ASCENDANT
    DEGREE = DetailedFields.DEGREE


class CriteriaAscendantRelationWithoutDescendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRel
        fields = [Fields.ASCENDANT, Fields.DEGREE]
