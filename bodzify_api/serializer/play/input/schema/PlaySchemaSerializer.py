#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.Play import Play, ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class FIELDS:
    CONTENT_OBJECT_UUID = ATTRIBUTES_LABEL.CONTENT_OBJECT + '_uuid'


class PlaySaveSchemaSerializer(serializers.ModelSerializer):
    content_object_uuid = serializers.CharField(max_length=settings.UUID_LEN, required=True)

    class Meta:
        model = Play
        fields = [FIELDS.CONTENT_OBJECT_UUID]

    def validate_content_object_uuid(self, object_id):
        user_id = self.context['request'].user.id
        if not Playlist.objects.filter(uuid=object_id, user_id=user_id).exists() \
                and not LibraryTrack.objects.filter(uuid=object_id, user_id=user_id).exists():
            raise serializers.ValidationError("Object with this ID does not exist or does not belong to the user.")
        return object_id
