from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.DescendantAwareUserUuidField import DescendantAwareUserUuidField
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer
from .Fields import Fields


class CriteriaPutSerializer(AppValidationSerializer, serializers.ModelSerializer):
    parent: serializers.Field = DescendantAwareUserUuidField(queryset=Criteria.objects.all(),
                                                             required=False,
                                                             allow_null=True)
    name = serializers.CharField()

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
