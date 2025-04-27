from rest_framework import serializers

from bodzify_api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from bodzify_api.serializer.model.spotify.artist.output.Fields import Fields


class SpotifyArtistSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyArtist
        fields = [
            Fields.SPOTIFY_ID,
            Fields.NAME,
            Fields.SPOTIFY_LINK,
            Fields.GENRES,
        ]
