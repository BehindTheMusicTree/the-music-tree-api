from rest_framework import serializers

from api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from api.serializer.model.criteria_lineage_rel.Fields import Fields


class CriteriaLineageRelDetailedSerializer(serializers.ModelSerializer):
    descendant = CriteriaMinimumSerializer()
    ascendant = CriteriaMinimumSerializer()

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.DESCENDANT,
                  Fields.ASCENDANT,
                  Fields.DEGREE]
