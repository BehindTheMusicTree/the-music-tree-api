from rest_framework import serializers

from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields
from bodzify_api.serializer.model.spotify.artist.output.detailed import SpotifyArtistDetailedSerializer


class SpotifyLibTrackDetailedSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    spotify_artists = SpotifyArtistDetailedSerializer(many=True, read_only=True)

    def get_genres(self, obj):
        # Get all unique genres from all artists
        genres = set()
        for artist in obj.spotify_artists.all():
            if artist.genres:
                genres.update(artist.genres)
        return list(genres)

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
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
            Fields.LAST_SYNCED_AT,
            Fields.IS_REMOVED,
            'genres'
        ]
