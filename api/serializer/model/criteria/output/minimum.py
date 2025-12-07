from rest_framework import serializers

from api.model.criteria.Criteria import Criteria
from api.serializer.AppInputSerializer import AppInputSerializer

from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME_PUBLIC = AvailableFields.NAME


class CriteriaMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [
            Fields.UUID,
            Fields.NAME_PUBLIC
        ]
