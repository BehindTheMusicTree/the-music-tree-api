from rest_framework import serializers

from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.serializer.model.spotify.artist.output.simple import SpotifyArtistSimpleSerializer
from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields


class SpotifyLibTrackDetailedSerializer(serializers.ModelSerializer):
    spotify_artists = SpotifyArtistSimpleSerializer(many=True, read_only=True)
    album = serializers.SerializerMethodField()

    class Meta:
        model = SpotifyLibTrack
        fields = [
            Fields.SPOTIFY_ID,
            Fields.NAME,
            Fields.DURATION_MS,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.POPULARITY,
            Fields.SPOTIFY_LINK,
            Fields.ALBUM,
            Fields.PREVIEW_URL,
            Fields.EXPLICIT,
            Fields.SPOTIFY_ARTISTS,
            Fields.IS_REMOVED,
            Fields.GENRES
        ]

    def get_album(self, obj):
        return obj.album.get('name') if obj.album else None
