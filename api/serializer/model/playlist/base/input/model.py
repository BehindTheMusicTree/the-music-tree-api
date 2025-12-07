from rest_framework import serializers

from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist
from api.serializer.AppInputSerializer import AppInputSerializer


class Fields:
    USER = PlayListFields.USER


class PlaylistModelSerializer(AppInputSerializer, serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [Fields.USER]
