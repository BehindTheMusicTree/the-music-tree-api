#!/usr/bin/env python

from bodzify_api.model.play.Play import Play, ATTRIBUTES_LABEL
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    CONTENT_TYPE = ATTRIBUTES_LABEL.CONTENT_TYPE
    OBJECT_ID = ATTRIBUTES_LABEL.OBJECT_ID


class PlaySaveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [FIELDS.USER,
                  FIELDS.CONTENT_TYPE,
                  FIELDS.OBJECT_ID]
