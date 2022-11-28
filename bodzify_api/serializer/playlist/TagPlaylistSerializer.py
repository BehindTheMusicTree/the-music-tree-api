from rest_framework import serializers

from bodzify_api.serializer.playlist.PlaylistSerializer import PlaylistSerializer

class TagPlaylistSerializer(PlaylistSerializer):
    additionalField = serializers.SerializerMethodField()

    def get_additional_field(self, obj):
        return('tag')

    class Meta(PlaylistSerializer.Meta):
        fields = PlaylistSerializer.Meta.fields + ('additional_field',)