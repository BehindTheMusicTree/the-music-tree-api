
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields
from bodzify_api.serializer.PutValidationSerializer import PutValidationSerializer
from .input import ManualPlaylistInputSerializer


class ManualPlaylistPutSerializer(ManualPlaylistInputSerializer, PutValidationSerializer):

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]
