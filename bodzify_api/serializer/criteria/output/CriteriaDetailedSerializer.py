#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.type.CriteriaTypeSerializer import CriteriaTypeSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT
    ROOT = ATTRIBUTES_LABEL.ROOT
    CHILDREN = ATTRIBUTES_LABEL.CHILDREN
    TYPE = ATTRIBUTES_LABEL.TYPE
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    type = CriteriaTypeSerializer()
    parent = CriteriaSimpleSerializer()
    root = CriteriaSimpleSerializer()  # type: ignore
    children = serializers.SerializerMethodField()

    class Meta:
        model = Criteria
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.PARENT,
                  FIELDS.ROOT,
                  FIELDS.CHILDREN,
                  FIELDS.TYPE,
                  FIELDS.ADDED_ON]

    def get_children(self, obj):
        return CriteriaSimpleSerializer(obj.get_children(), many=True).data
