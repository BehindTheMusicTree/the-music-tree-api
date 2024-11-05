
from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as BasePlaylistFields


class ChildPlaylistModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data[BasePlaylistFields.USER] = user
        return super().create(validated_data)
