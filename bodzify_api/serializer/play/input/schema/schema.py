#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.Play import Play, AttributesLabel
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class Fields:
    CONTENT_OBJECT_UUID = AttributesLabel.CONTENT_OBJECT + '_uuid'


class PlaySchemaSerializer(serializers.ModelSerializer):
    content_object_uuid = serializers.CharField(max_length=settings.UUID_LEN, required=True)

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]

    def validate_content_object_uuid(self, object_id):
        user_id = self.context['request'].user.id
        if not BasePlaylist.objects.filter(uuid=object_id, user_id=user_id).exists() \
                and not LibraryTrack.objects.filter(uuid=object_id, user_id=user_id).exists():
            raise serializers.ValidationError(
                {Fields.CONTENT_OBJECT_UUID: "Object with this ID does not exist or does not belong to the user."})
        return object_id
