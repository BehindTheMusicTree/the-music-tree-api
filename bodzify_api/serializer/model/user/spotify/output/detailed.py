from rest_framework import serializers

from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from .Fields import Fields


class SpotifyUserDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyUser
        fields = [
            Fields.SPOTIFY_ID,
            Fields.EMAIL,
            Fields.SPOTIFY_PROFILE,
            Fields.DISPLAY_NAME,
            Fields.FOLLOWERS,
            Fields.HREF,
            Fields.IMAGES,
            Fields.TYPE,
            Fields.URI,
            Fields.SPOTIFY_LIBRARY_LAST_SYNCED_AT,
        ]
