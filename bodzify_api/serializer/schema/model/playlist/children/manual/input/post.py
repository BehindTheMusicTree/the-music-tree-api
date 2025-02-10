
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields
from bodzify_api.serializer.schema.model.playlist.children.manual.input.input import ManualPlaylistInputSerializer


class ManualPlaylistPostSerializer(ManualPlaylistInputSerializer):

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]
