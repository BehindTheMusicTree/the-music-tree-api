from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME_PUBLIC = AvailableFields.NAME


class CriteriaMinimumSerializer(AppValidationSerializer, serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [
            Fields.UUID,
            Fields.NAME_PUBLIC
        ]
