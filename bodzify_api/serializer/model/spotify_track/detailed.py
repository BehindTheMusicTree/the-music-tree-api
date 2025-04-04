from rest_framework import serializers

from bodzify_api.model.spotify_resource.children.track.SpotifyTrack import SpotifyTrack
from bodzify_api.serializer.model.spotify_track.Fields import Fields


class SpotifyTrackDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyTrack
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.DURATION_MS,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.POPULARITY,
            Fields.SPOTIFY_LINK,
            Fields.ALBUM,
            Fields.PREVIEW_URL,
            Fields.EXPLICIT,
            Fields.SPOTIFY_ARTISTS,
            Fields.SPOTIFY_ID,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
            Fields.LAST_SYNCED_AT,
            Fields.IS_REMOVED
        ]
