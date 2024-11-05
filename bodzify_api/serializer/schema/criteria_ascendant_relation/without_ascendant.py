from bodzify_api.model.criteria_acendant_rel.CriteriaAscendantRel import CriteriaAscendantRel
from bodzify_api.serializer.schema.criteria_ascendant_relation.Fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria_ascendant_relation.detailed import CriteriaAscendantRelationDetailedSerializer


class Fields:
    DESCENDANT = AvailableFields.DESCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaAscendantRelationWithoutAscendantSerializer(CriteriaAscendantRelationDetailedSerializer):

    class Meta:
        model = CriteriaAscendantRel
        fields = [Fields.DESCENDANT, Fields.DEGREE]
