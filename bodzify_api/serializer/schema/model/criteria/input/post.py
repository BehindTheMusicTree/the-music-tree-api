
from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from .Fields import Fields


class CriteriaPostSerializer(AppValidationSerializer, serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
