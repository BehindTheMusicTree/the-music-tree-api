
from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import Fields as BasePlaylistFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist


class Fields:
    USER = BasePlaylistFields.USER


class BasePlaylistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.USER]
