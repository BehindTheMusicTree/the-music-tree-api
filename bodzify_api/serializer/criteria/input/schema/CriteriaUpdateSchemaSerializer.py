#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class CriteriaPutSchemaSerializer(InputModelSerializer):

    class Meta:
        model = Criteria
        fields = [
            ATTRIBUTES_LABEL.NAME, 
            ATTRIBUTES_LABEL.PARENT,
        ]

    def validate_parent(self, value):
        instance = self.instance

        if instance and value:
            if instance == value:
                raise serializers.ValidationError("Cannot set the new parent as the genre itself.")
            elif value.is_descendant_of(instance):
                raise serializers.ValidationError("Cannot set the new parent as one of the genre's descendants.")
        return value