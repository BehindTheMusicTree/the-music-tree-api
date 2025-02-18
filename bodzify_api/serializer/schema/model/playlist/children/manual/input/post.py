
from bodzify_api import settings
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.schema.model.playlist.children.manual.input.input import ManualPlaylistInputSerializer


class ManualPlaylistPostSerializer(ManualPlaylistInputSerializer):
    name = AppCharField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, source=ModelFields.NAME_INTERNAL)

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]
