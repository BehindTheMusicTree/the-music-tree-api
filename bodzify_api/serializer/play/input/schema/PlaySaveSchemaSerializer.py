#!/usr/bin/env python

from bodzify_api.model.play.Play import Play, ATTRIBUTES_LABEL
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    CONTENT_OBJECT_UUID = ATTRIBUTES_LABEL.CONTENT_OBJECT + '_uuid'


class PlaySaveSchemaSerializer(serializers.ModelSerializer):
    content_object_uuid = serializers.CharField(max_length=22, required=True)

    class Meta:
        model = Play
        fields = [FIELDS.USER, FIELDS.CONTENT_OBJECT_UUID]

    def validate_content_object_uuid(self, object_id):
        user_id = self.initial_data[FIELDS.USER]
        if not Playlist.objects.filter(uuid=object_id, user_id=user_id).exists():
            raise serializers.ValidationError("Object with this ID does not exist or does not belong to the user.")
        return object_id
