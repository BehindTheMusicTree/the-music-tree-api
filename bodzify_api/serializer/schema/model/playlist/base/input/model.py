from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer


class Fields:
    USER = PlaylistFields.USER


class PlaylistModelSerializer(AppModelSerializer):

    class Meta:
        model = Playlist
        fields = [Fields.USER]
