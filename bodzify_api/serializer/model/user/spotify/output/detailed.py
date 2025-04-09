from rest_framework import serializers

from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.model.user.spotify.Fields import Fields


class SpotifyUserDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyUser
        fields = [
            Fields.ID,
            Fields.EMAIL,
            Fields.USERNAME,
            Fields.SPOTIFY_ID,
            Fields.SPOTIFY_PROFILE,
            Fields.SPOTIFY_LIBRARY_LAST_SYNCED_AT,
            Fields.SPOTIFY_SYNC_IN_PROGRESS,
            Fields.DISPLAY_NAME,
            Fields.FOLLOWERS,
            Fields.HREF,
            Fields.IMAGES,
            Fields.TYPE,
            Fields.URI
        ]
