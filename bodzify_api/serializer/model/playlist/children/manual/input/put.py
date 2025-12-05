
from bodzify_api import settings
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.PutSerializer import PutSerializer
from bodzify_api.serializer.field.UniquePerUserNameField import UniquePerUserNameField

from .input import ManualPlaylistInputSerializer


class ManualPlaylistPutSerializer(ManualPlaylistInputSerializer, PutSerializer):
    name = UniquePerUserNameField(
        model=ManualPlaylist,
        max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX,
        allow_blank=False,
        required=False
    )

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]
