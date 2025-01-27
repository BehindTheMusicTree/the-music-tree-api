
from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist


class Fields:
    NAME = PlaylistFields.NAME_PUBLIC


class ManualPlaylistSchemaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX,
                                 required=False,
                                 allow_blank=True,
                                 allow_null=True)

    class Meta:
        model = ManualPlaylist
        fields = [Fields.NAME]
