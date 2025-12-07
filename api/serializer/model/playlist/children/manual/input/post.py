
from api import settings
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.serializer.field.UniquePerUserNameField import UniquePerUserNameField
from api.serializer.model.playlist.children.manual.input.input import ManualPlaylistInputSerializer

from .Fields import Fields


class ManualPlaylistPostSerializer(ManualPlaylistInputSerializer):
    name = UniquePerUserNameField(max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX,
                                  source=Fields.NAME_INTERNAL,
                                  model=ManualPlaylist)

    class Meta:
        model = ManualPlaylist
        fields = [Fields.NAME_PUBLIC]
