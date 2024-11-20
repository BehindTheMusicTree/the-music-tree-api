
from bodzify_api.model.playlist.children.manual.ManualPlaylist import Fields, ManualPlaylist
from bodzify_api.serializer.schema.model.playlist.children.model import ChildPlaylistModelSerializer


class Fields:
    NAME = Fields.NAME


class ManualPlaylistModelSerializer(ChildPlaylistModelSerializer):

    class Meta:
        model = ManualPlaylist
        fields = [Fields.NAME]
