from typing import TYPE_CHECKING, Dict

from django.core.exceptions import ImproperlyConfigured

from bodzify_api.model.lib_track_mixin.Fields import \
    Fields as LibTrackMixinFields
from bodzify_api.model.lib_track_mixin.LibTrackMixinWithInternalNameManager import \
    LibTrackMixinWithInternalNameManager
from bodzify_api.utils.audio_metadata.manager.MetadataManager import \
    METADATA_ARTISTS_SEPARATION_CHAR

if TYPE_CHECKING:
    from bodzify_api.model.user.User import User

    from .Artist import Artist


class ArtistManager(LibTrackMixinWithInternalNameManager['Artist']):
    model: type['Artist']

    def get_default_ordering(self) -> list[str]:
        return [LibTrackMixinFields.NAME_INTERNAL]

    def get_artists_names_list_from_metadata_str(self, names_str: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_str.split(METADATA_ARTISTS_SEPARATION_CHAR)
        names = []
        for name_with_eventual_spaces_around in names_with_eventual_spaces_around_and_duplicates:
            name = name_with_eventual_spaces_around.strip()
            if name != "" and names.count(name) == 0:
                names.append(name)
        return names

    def get_artists_list_from_names_after_eventual_creation(
            self, user: 'User', artists_names_list: str) -> list['Artist']:
        return [self.get_or_create(user=user, name=artist_name)[0] for artist_name in artists_names_list] \
            if len(artists_names_list) > 0 else []

    def get_artists_list_from_metadata_str_after_eventual_creation(
            self, user: 'User', artists_names_str: str) -> list['Artist']:
        if not user:
            raise ImproperlyConfigured("User must be provided")

        names_list = self.get_artists_names_list_from_metadata_str(artists_names_str)
        artists = []
        for name in names_list:
            artists.append(self.get_or_create(user=user, name=name)[0])
        return artists

    def delete_instance(self, instance: 'Artist'):
        self.delete_instance_with_albums_and_tracks(instance)

    def delete_instance_with_albums_and_tracks(self, instance: 'Artist') -> tuple[int, Dict[str, int]]:
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        # Keep deletion order for rollback tests

        for album in instance.albums.all():
            Album.objects.delete_instance_with_tracks_and_eventually_artists(album)

        for lib_track in instance.lib_tracks.all():
            LibraryTrack.objects.delete_instance_with_checking_album_and_artists_potential_deletion(lib_track)

        return instance.delete()

    def delete_instance_if_nothing_linked(self, instance: 'Artist') -> tuple[int, Dict[str, int]]:
        if instance.albums.count() == 0:
            if instance.lib_tracks.count() == 0:
                return instance.delete()
        return 0, {}
