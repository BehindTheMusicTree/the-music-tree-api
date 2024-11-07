from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from bodzify_api.serializer.schema.criteria_ascendant_relation.Fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria_ascendant_relation.detailed import CriteriaLineageRelationDetailedSerializer


class Fields:
    DESCENDANT = AvailableFields.DESCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaLineageRelationWithoutAscendantSerializer(CriteriaLineageRelationDetailedSerializer):

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.DESCENDANT, Fields.DEGREE]
