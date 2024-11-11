
from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.Playlist import Playlist


class Fields:
    USER = PlaylistFields.USER


class PlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [Fields.USER]
