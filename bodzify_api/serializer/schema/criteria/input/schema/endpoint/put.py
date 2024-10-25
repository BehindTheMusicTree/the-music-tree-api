#!/usr/bin/env python

from rest_framework.exceptions import ValidationError

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.schema.criteria.input.schema.schema import CriteriaSchemaSerializer
from bodzify_api.serializer.schema.criteria.input.schema.schema import Fields as SchemaFields
from bodzify_api.serializer.schema.endpoint import InputEndpointSerializer


class Fields:
    NAME = SchemaFields.NAME
    PARENT = SchemaFields.PARENT


class CriteriaPutSerializer(CriteriaSchemaSerializer, InputEndpointSerializer):

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]

    def validate(self, data):
        instance = self.instance
        value = data.get(Fields.PARENT)

        if instance and value:
            error_message = None
            if instance == value:
                error_message = "Cannot set the new parent as the criteria itself."
            elif value.is_descendant_of(instance):
                error_message = "Cannot set the new parent as one of the criteria's descendants."

            if error_message:
                raise ValidationError({Fields.PARENT: error_message})

        return super().validate(data)
