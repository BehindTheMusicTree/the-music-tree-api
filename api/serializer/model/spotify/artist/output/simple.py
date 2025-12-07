from rest_framework import serializers

from api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from api.serializer.model.spotify.artist.output.Fields import Fields


class SpotifyArtistSimpleSerializer(serializers.ModelSerializer):
    spotify_link = serializers.SerializerMethodField()

    def get_spotify_link(self, obj):
        return getattr(obj, Fields.SPOTIFY_LINK, None)

    class Meta:
        model = SpotifyArtist
        fields = [
            Fields.SPOTIFY_ID,
            Fields.NAME,
            Fields.POPULARITY,
            Fields.SPOTIFY_LINK,
            Fields.GENRES,
            Fields.IMAGES,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
        ]
