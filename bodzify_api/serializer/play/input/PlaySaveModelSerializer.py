#!/usr/bin/env python

from bodzify_api.model.Play import Play, ATTRIBUTES_LABEL
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    CONTENT_TYPE = ATTRIBUTES_LABEL.CONTENT_TYPE
    OBJECT_UUID = ATTRIBUTES_LABEL.OBJECT_UUID


class PlaySaveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [FIELDS.USER,
                  FIELDS.CONTENT_TYPE,
                  FIELDS.OBJECT_UUID]
