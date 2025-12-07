from rest_framework import serializers

from api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from .Fields import Fields as AvailableFields


class Fields:
    DESCENDANT = AvailableFields.DESCENDANT
    DEGREE = AvailableFields.DEGREE


class CriteriaLineageRelWithoutAscendantSerializer(serializers.ModelSerializer):
    descendant = CriteriaMinimumSerializer()

    class Meta:
        model = CriteriaLineageRel
        fields = [Fields.DESCENDANT, Fields.DEGREE]
