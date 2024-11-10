from rest_framework import serializers

from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from .Fields import Fields


class CriteriaTypeDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriteriaType
        fields = [Fields.LABEL]
