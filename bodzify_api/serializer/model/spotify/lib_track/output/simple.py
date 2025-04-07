from rest_framework import serializers

from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields
from bodzify_api.serializer.model.spotify.artist.output.detailed import SpotifyArtistDetailedSerializer


class SpotifyLibTrackSimpleSerializer(serializers.ModelSerializer):
    spotify_artists = SpotifyArtistDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = SpotifyLibTrack
        fields = [
            Fields.SPOTIFY_ID,
            Fields.NAME,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.SPOTIFY_LINK,
            Fields.ALBUM,
            Fields.SPOTIFY_ARTISTS,
            Fields.CREATED_ON,
            Fields.LAST_SYNCED_AT,
            Fields.IS_REMOVED,
            Fields.GENRES
        ]
