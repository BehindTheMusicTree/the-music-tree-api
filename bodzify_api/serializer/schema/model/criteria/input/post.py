
from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from .Fields import Fields


class CriteriaPostSerializer(AppValidationSerializer, serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=settings.CRITERIA_NAME_LEN_MAX,
        allow_blank=False
    )

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
