from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.playlist.PlaylistTypeSerializer import PlaylistTypeSerializer


class ParentPlaylistSerializer(serializers.ModelSerializer):
    type = PlaylistTypeSerializer()
    trackCount = serializers.IntegerField(source='librarytrack_set.count')

    class Meta:
        model = Playlist
        fields = [
            "uuid",
            "name",
            "type",
            "criteria",
            "addedOn",
            "trackCount"
        ]


class PlaylistSerializer(ParentPlaylistSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        if obj.parent is not None:
            return ParentPlaylistSerializer(obj.parent).data
        else:
            return None


    class Meta:
        model = Playlist    
        fields = [
            "uuid",
            "name",
            "type",
            "criteria",
            "parent",
            "addedOn",
            "trackCount"
        ]
