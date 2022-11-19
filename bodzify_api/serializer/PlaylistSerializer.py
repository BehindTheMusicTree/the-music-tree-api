from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist

class PlaylistSerializer(serializers.Serializer):

    trackCount = serializers.IntegerField(source='librarytrack_set.count')  
    class Meta:
        model = Playlist
        fields = [
            "name", 
            "type", 
            "trackCount",
            "duration",
            "url"]