from typing import TYPE_CHECKING, Optional
from bodzify_api.model.lib_track_mixin.LibTrackMixinManager import LibTrackMixinManager
from bodzify_api.model.user.User import User
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.artist.Artist import Artist
    from .Album import Album


class AlbumManager(LibTrackMixinManager):
    model: 'Album'

    def _get_instance_from_name_and_artists_list_after_having_eventually_created_instance(
            self, user: User, album_name: str, album_artists: list) -> Optional['Album']:

        album_queryset = self.model.objects.filter(user=user, name=album_name)
        if len(album_artists) > 0:
            for album_artist in album_artists:
                album_queryset = album_queryset.filter(album_artists__in=[album_artist])
        else:
            album_queryset = album_queryset.filter(album_artists=None)

        return self.create_instance_with_album_artists_list(
            user=user, album_name=album_name, album_artists_list=album_artists) \
            if album_queryset.count() == 0 else album_queryset.first()

    def get_default_ordering(self) -> list[str]:
        return [Fields.NAME]

    def create_instance_with_album_artists_list(
            self, user: User, album_name: str, album_artists_list: list['Artist']) -> 'Album':
        album: Album = self.create(user=user, name=album_name)
        if album_artists_list:
            album.album_artists.set(album_artists_list)
        return album

    def get_album_from_name_and_album_artists_names_list_after_eventual_creations(
            self, user: User, album_name: str, album_artists_names_list: list) -> Optional['Album']:
        from bodzify_api.model.artist.Artist import Artist
        album_artists = \
            [Artist.objects.get_or_create(user=user, name=artist_name)[0] for artist_name in album_artists_names_list] \
            if album_artists_names_list and len(album_artists_names_list) > 0 else []

        return self._get_instance_from_name_and_artists_list_after_having_eventually_created_instance(
            user=user, album_name=album_name, album_artists=album_artists)
