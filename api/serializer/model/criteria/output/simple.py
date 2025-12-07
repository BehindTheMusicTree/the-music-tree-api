from rest_framework import serializers

from api.model.criteria.Criteria import Criteria
from api.serializer.AppInputSerializer import AppInputSerializer
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    PARENT = AvailableFields.PARENT
    CREATED_ON = AvailableFields.CREATED_ON


class CriteriaSimpleSerializer(AppInputSerializer, serializers.ModelSerializer):
    parent = CriteriaMinimumSerializer()

    class Meta:
        model = Criteria
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.PARENT,
            Fields.CREATED_ON
        ]
