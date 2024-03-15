#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.type.CriteriaTypeSerializer \
    import CriteriaTypeSerializer, FIELDS as CRITERIA_TYPE_FIELDS
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutTracksSerializer \
    import CriteriaPlaylistWithoutTracksSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT
    ROOT = ATTRIBUTES_LABEL.ROOT
    CHILDREN = ATTRIBUTES_LABEL.CHILDREN
    TYPE = ATTRIBUTES_LABEL.TYPE
    TYPE_LABEL = CRITERIA_TYPE_FIELDS.LABEL
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    CRITERIA_PLAYLIST = ATTRIBUTES_LABEL.CRITERIA_PLAYLIST


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    type = CriteriaTypeSerializer()
    parent = CriteriaSimpleSerializer()
    root = CriteriaSimpleSerializer()  # type: ignore
    children = serializers.SerializerMethodField()
    criteria_playlist = CriteriaPlaylistWithoutTracksSerializer()

    class Meta:
        model = Criteria
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.PARENT,
                  FIELDS.ROOT,
                  FIELDS.CHILDREN,
                  FIELDS.TYPE,
                  FIELDS.ADDED_ON,
                  FIELDS.CRITERIA_PLAYLIST]

    def get_children(self, obj):
        return CriteriaSimpleSerializer(obj.get_children(), many=True).data
