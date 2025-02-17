from typing import Dict, Any

from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.foreign_key.DescendantAwareField import DescendantAwareField
from .Fields import Fields


class CriteriaPostSerializer(ModelSerializer, AppValidationSerializer):
    """
    Serializer for creating new Criteria objects.
    Handles validation of name and parent fields.
    """
    name = AppCharField(max_length=settings.CRITERIA_NAME_LEN_MAX, allow_blank=False)
    parent = DescendantAwareField(
        queryset=Criteria.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]