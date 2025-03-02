from typing import TYPE_CHECKING


from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields
from bodzify_api.model.lib_track_mixin.LibTrackMixinWithInternalNameManager import LibTrackMixinWithInternalNameManager


if TYPE_CHECKING:
    from bodzify_api.model.user.User import User

    from .Artist import Artist


class ArtistManager(LibTrackMixinWithInternalNameManager['Artist']):
    model: type['Artist']

    def get_default_ordering(self) -> list[str]:
        return [LibTrackMixinFields.NAME_INTERNAL]

    def get_artists_list_from_names_after_potential_creation(self, user: 'User', artists_names: str) -> list['Artist']:
        return [self.get_or_create(user=user, name=artist_name)[0] for artist_name in artists_names] \
            if len(artists_names) > 0 else []

    def delete_instance(self, instance: 'Artist'):
        self.delete_instance_with_albums_and_tracks(instance)

    def delete_instance_with_albums_and_tracks(self, instance: 'Artist') -> tuple[int, dict[str, int]]:
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

        # Keep deletion order for rollback tests

        for album in instance.albums.all():
            Album.objects.delete_instance_with_tracks_and_potentially_artists(album)

        for lib_track in instance.lib_tracks.all():
            LibraryTrack.objects.delete_instance_with_checking_album_and_artists_potential_deletion(lib_track)

        return instance.delete()

    def delete_instance_if_nothing_linked(self, instance: 'Artist') -> tuple[int, dict[str, int]]:
        if instance.albums.count() == 0:
            if instance.lib_tracks.count() == 0:
                return instance.delete()
        return 0, {}
