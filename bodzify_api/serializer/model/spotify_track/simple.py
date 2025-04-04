from rest_framework import serializers

from bodzify_api.model.spotify_resource.children.track.SpotifyTrack import SpotifyTrack
from bodzify_api.serializer.model.spotify_track.Fields import Fields


class SpotifyTrackSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyTrack
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.SPOTIFY_LINK,
            Fields.ALBUM,
            Fields.SPOTIFY_ARTISTS,
            Fields.CREATED_ON,
            Fields.LAST_SYNCED_AT,
            Fields.IS_REMOVED
        ]
