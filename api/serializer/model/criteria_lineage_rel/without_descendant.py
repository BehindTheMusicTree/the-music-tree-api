
from api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from api.serializer.model.criteria_lineage_rel.detailed import CriteriaLineageRelDetailedSerializer
from api.serializer.model.criteria_lineage_rel.Fields import Fields as AvailableFields


class Fields:
    ASCENDANT = AvailableFields.ASCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaLineageRelWithoutDescendantSerializer(CriteriaLineageRelDetailedSerializer):
    ascendant = CriteriaMinimumSerializer()

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.ASCENDANT, Fields.DEGREE]
