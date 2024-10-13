#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import AttributesLabels, BasePlaylist
from bodzify_api.serializer.criteria.type.detailed import CriteriaTypeSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    TYPE_LABEL = AttributesLabels.TYPE_LABEL


class BasePlaylistWithOnlyNameAndType(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL,]
