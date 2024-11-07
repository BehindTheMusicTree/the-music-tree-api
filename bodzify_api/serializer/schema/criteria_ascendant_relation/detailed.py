
from rest_framework import serializers

from bodzify_api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from bodzify_api.serializer.schema.criteria_ascendant_relation.Fields import Fields
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer


class CriteriaLineageRelationDetailedSerializer(serializers.ModelSerializer):
    descendant = CriteriaMinimumSerializer()
    ascendant = CriteriaMinimumSerializer()

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.DESCENDANT,
                  Fields.ASCENDANT,
                  Fields.DEGREE]
