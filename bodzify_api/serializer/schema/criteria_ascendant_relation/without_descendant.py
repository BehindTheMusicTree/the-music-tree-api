
from bodzify_api.model.criteria_acendant_rel.CriteriaAscendantRel import CriteriaAscendantRel
from bodzify_api.serializer.schema.criteria_ascendant_relation.Fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria_ascendant_relation.detailed import CriteriaAscendantRelationDetailedSerializer


class Fields:
    ASCENDANT = AvailableFields.ASCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaAscendantRelationWithoutDescendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRel
        fields = [Fields.ASCENDANT, Fields.DEGREE]
