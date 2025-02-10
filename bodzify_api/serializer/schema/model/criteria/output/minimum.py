from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME_PUBLIC = AvailableFields.NAME
    NAME_INTERNAL = AvailableFields.NAME_INTERNAL


class CriteriaMinimumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME_PUBLIC,]
