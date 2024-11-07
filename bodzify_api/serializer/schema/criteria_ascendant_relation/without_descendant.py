
from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from bodzify_api.serializer.schema.criteria_ascendant_relation.Fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria_ascendant_relation.detailed import CriteriaLineageRelationDetailedSerializer


class Fields:
    ASCENDANT = AvailableFields.ASCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaLineageRelationWithoutDescendantSerializer(CriteriaLineageRelationDetailedSerializer):

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.ASCENDANT, Fields.DEGREE]
