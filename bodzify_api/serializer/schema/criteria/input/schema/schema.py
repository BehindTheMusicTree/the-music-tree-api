
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bodzify_api.model.criteria.Criteria import Criteria, Fields as ModelFields


class Fields:
    NAME = ModelFields.NAME
    PARENT = ModelFields.PARENT


class CriteriaSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]

    def validate(self, data):
        user = self.context['request'].user
        if Fields.NAME in data and Criteria.objects.filter(user=user, name=data[Fields.NAME]).exists():
            raise ValidationError({Fields.NAME: "Name already exists"})
        return super().validate(data)
