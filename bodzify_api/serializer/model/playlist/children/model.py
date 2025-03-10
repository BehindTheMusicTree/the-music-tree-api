from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.serializer.AppSerializer import AppSerializer


class ChildPlaylistModelSerializer(AppSerializer, serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data[PlayListFields.USER] = user
        return super().create(validated_data)
