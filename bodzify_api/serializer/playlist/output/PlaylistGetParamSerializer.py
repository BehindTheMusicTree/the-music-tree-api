#!/usr/bin/env python

from django.forms import ValidationError
from rest_framework import serializers
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import \
    CriteriaPlaylist, ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.CriteriaPlaylist import \
    TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL

class ATTRIBUTES_LABEL:
    TYPE = "type"


class PlaylistGetParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)

    class Meta:
        fields = [PLAYLIST_ATTRIBUTES_LABEL.NAME, ATTRIBUTES_LABEL.TYPE]

    def validate(self, data):
        if ATTRIBUTES_LABEL.TYPE in data:
            type = data[ATTRIBUTES_LABEL.TYPE]
            if type not in [SimplePlaylist.TYPE_LABEL,
                            CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
                            CRITERIA_PLAYLIST_TYPES_LABEL.TAG]:
                raise ValidationError("Invalid type value")
            else:
                parent = data[CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT]
                if parent is not None and type not in [CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
                                                       CRITERIA_PLAYLIST_TYPES_LABEL.TAG]:
                    raise ValidationError("Parent parameter is not allowed for this type")
        return super().validate(data)
