
from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from bodzify_api.serializer.schema.criteria_lineage_rel.Fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria_lineage_rel.detailed import CriteriaLineageRelDetailedSerializer


class Fields:
    ASCENDANT = AvailableFields.ASCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaLineageRelWithoutDescendantSerializer(CriteriaLineageRelDetailedSerializer):

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.ASCENDANT, Fields.DEGREE]
