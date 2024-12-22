from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.DescendantAwareUserUuidField import DescendantAwareUserUuidField
from bodzify_api.serializer.schema.base_input.AppInputModelSerializer import AppInputModelSerializer
from .Fields import Fields


class CriteriaPutSerializer(AppInputModelSerializer):
    parent: serializers.Field = DescendantAwareUserUuidField(
        queryset=Criteria.objects.all(),
        required=False,
        allow_null=True
    )
    name = serializers.CharField(source='_name')

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
