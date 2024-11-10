from typing import TYPE_CHECKING

from bodzify_api.model.lib_track_mixin.LibTrackMixinManager import LibTrackMixinManager
from bodzify_api.model.user.User import User
from bodzify_api.utils.audio_metadata.MetadataManager import METADATA_ARTISTS_SEPARATION_CHAR
from .Fields import Fields

if TYPE_CHECKING:
    from .Artist import Artist


class ArtistManager(LibTrackMixinManager):

    def get_artists_names_list_from_str(self, names_str: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_str.split(METADATA_ARTISTS_SEPARATION_CHAR)
        names = []
        for name_with_eventual_spaces_around in names_with_eventual_spaces_around_and_duplicates:
            name = name_with_eventual_spaces_around.strip()
            if name != "" and names.count(name) == 0:
                names.append(name)
        return names

    def get_default_ordering(self):
        return [Fields.NAME]

    def get_artists_list_from_names_str_after_eventual_creation(
            self, user: User, artists_names_str: str) -> list['Artist']:
        artists_names_list = self.get_artists_names_list_from_str(artists_names_str)
        return [self.get_or_create(user=user, name=artist_name)[0] for artist_name in artists_names_list] \
            if len(artists_names_list) > 0 else []
