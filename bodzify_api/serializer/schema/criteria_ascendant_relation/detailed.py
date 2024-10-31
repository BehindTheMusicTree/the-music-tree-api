
from rest_framework import serializers

from bodzify_api.model.criteria.CriteriaAscendantRel import CriteriaAscendantRel
from bodzify_api.serializer.schema.criteria_ascendant_relation.fields import Fields
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer


class CriteriaAscendantRelationDetailedSerializer(serializers.ModelSerializer):
    descendant = CriteriaMinimumSerializer()
    ascendant = CriteriaMinimumSerializer()

    class Meta:
        model = CriteriaAscendantRel
        fields = [Fields.DESCENDANT,
                  Fields.ASCENDANT,
                  Fields.DEGREE]
