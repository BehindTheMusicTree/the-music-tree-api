from rest_framework import serializers

from bodzify_api.model.spotify_resource.children.track.SpotifyTrack import SpotifyTrack
from bodzify_api.model.spotify_resource.children.track.Fields import Fields
from bodzify_api.view.serializer.model.spotify_album.simple import SpotifyAlbumSimpleSerializer
from bodzify_api.view.serializer.model.spotify_artist.simple import SpotifyArtistSimpleSerializer


class SpotifyTrackSimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for Spotify tracks with basic information."""

    album = SpotifyAlbumSimpleSerializer(read_only=True)
    artists = SpotifyArtistSimpleSerializer(many=True, read_only=True, source='spotify_artists')
    duration = serializers.SerializerMethodField()
    is_removed = serializers.BooleanField(source=Fields.IS_REMOVED)
    last_synced_at = serializers.DateTimeField(source=Fields.LAST_SYNCED_AT)

    class Meta:
        model = SpotifyTrack
        fields = [
            'id',
            Fields.SPOTIFY_ID,
            Fields.NAME,
            'duration',
            Fields.POPULARITY,
            Fields.SPOTIFY_LINK,
            'album',
            'artists',
            Fields.PREVIEW_URL,
            Fields.EXPLICIT,
            Fields.IS_REMOVED,
            Fields.LAST_SYNCED_AT,
        ]

    def get_duration(self, obj: SpotifyTrack) -> str:
        return obj.format_duration()
