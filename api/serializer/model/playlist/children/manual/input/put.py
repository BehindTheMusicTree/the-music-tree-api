
from api import settings
from api.model.playlist.children.manual.Fields import Fields as ModelFields
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.serializer.PutSerializer import PutSerializer
from api.serializer.field.UniquePerUserNameField import UniquePerUserNameField

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
