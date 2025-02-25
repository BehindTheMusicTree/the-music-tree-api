
from bodzify_api.model.playlist.children.manual.Fields import     Fields as ModelFields
from bodzify_api.model.playlist.children.manual.ManualPlaylist import     ManualPlaylist
from bodzify_api.serializer.PutSerializer import PutSerializer

from .input import ManualPlaylistInputSerializer


class ManualPlaylistPutSerializer(ManualPlaylistInputSerializer, PutSerializer):

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]
