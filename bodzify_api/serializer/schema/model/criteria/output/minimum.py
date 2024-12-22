from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class CriteriaMinimumSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='_name')

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,]