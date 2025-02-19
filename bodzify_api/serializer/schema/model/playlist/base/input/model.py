from rest_framework import serializers

from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.AppSerializer import AppSerializer


class Fields:
    USER = PlaylistFields.USER


class PlaylistModelSerializer(AppSerializer, serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [Fields.USER]
