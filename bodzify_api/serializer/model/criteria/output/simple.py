from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    PARENT = AvailableFields.PARENT
    CREATED_ON = AvailableFields.CREATED_ON


class CriteriaSimpleSerializer(AppSerializer, serializers.ModelSerializer):
    parent = CriteriaMinimumSerializer()

    class Meta:
        model = Criteria
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.PARENT,
            Fields.CREATED_ON
        ]
