from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.base_input.AppInputModelSerializer import AppInputModelSerializer

from .Fields import Fields


class CriteriaPostSerializer(AppInputModelSerializer):
    name = serializers.CharField(source=Fields.NAME_INTERNAL)

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
