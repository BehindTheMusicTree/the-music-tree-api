#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Play import Play, Fields as ModelFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class Fields:
    CONTENT_OBJECT_UUID = ModelFields.CONTENT_OBJECT + '_uuid'


class PlaySchemaSerializer(serializers.ModelSerializer):
    content_object_uuid = serializers.UUIDField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]

    def validate_content_object_uuid(self, object_id):
        user = self.context['request'].user
        if not BasePlaylist.objects.filter(user=user, uuid=object_id).exists() \
                and not LibraryTrack.objects.filter(user=user, uuid=object_id).exists():
            raise serializers.ValidationError(
                {Fields.CONTENT_OBJECT_UUID: "Object with this ID does not exist or does not belong to the user."})
        return object_id
